#!/usr/bin/env python3
"""Process raw Notion API response into stats JSON for the dashboard widget."""

import json
from datetime import datetime, timedelta
from collections import defaultdict

def main():
    with open("raw_data.json", "r") as f:
        raw = json.load(f)

    results = raw.get("results", [])

    # Parse sessions
    sessions = []
    for page in results:
        props = page.get("properties", {})

        # Session Name (title)
        name_prop = props.get("Session Name", {})
        title_parts = name_prop.get("title", [])
        name = "".join(t.get("plain_text", "") for t in title_parts) if title_parts else "Untitled"

        # Type (select)
        type_prop = props.get("Type", {})
        type_sel = type_prop.get("select")
        session_type = type_sel["name"] if type_sel else "Unknown"

        # Focus Rating (select)
        rating_prop = props.get("Focus Rating", {})
        rating_sel = rating_prop.get("select")
        rating_name = rating_sel["name"] if rating_sel else ""
        # Count stars
        rating = rating_name.count("⭐")

        # Status (select)
        status_prop = props.get("Status", {})
        status_sel = status_prop.get("select")
        status = status_sel["name"] if status_sel else "Unknown"

        # Time Span (date)
        time_prop = props.get("Time Span", {})
        date_info = time_prop.get("date")
        start_date = None
        if date_info and date_info.get("start"):
            try:
                start_str = date_info["start"]
                # Handle both date and datetime formats
                if "T" in start_str:
                    start_date = datetime.fromisoformat(start_str.replace("Z", "+00:00"))
                else:
                    start_date = datetime.strptime(start_str, "%Y-%m-%d")
            except (ValueError, TypeError):
                start_date = None

        # Created time as fallback
        created = page.get("created_time", "")
        if not start_date and created:
            try:
                start_date = datetime.fromisoformat(created.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                start_date = None

        sessions.append({
            "name": name,
            "type": session_type,
            "rating": rating,
            "status": status,
            "date": start_date,
        })

    now = datetime.now()
    today = now.date()

    # Total sessions
    total_sessions = len(sessions)

    # Average rating (only rated sessions)
    rated = [s["rating"] for s in sessions if s["rating"] > 0]
    avg_rating = round(sum(rated) / len(rated), 1) if rated else 0

    # Flow states (3-star sessions)
    flow_states = sum(1 for s in sessions if s["rating"] == 3)

    # Day streak (consecutive days with at least 1 session, counting back from today)
    session_dates = set()
    for s in sessions:
        if s["date"]:
            session_dates.add(s["date"].date() if hasattr(s["date"], "date") else s["date"])

    streak = 0
    check_date = today
    while check_date in session_dates:
        streak += 1
        check_date -= timedelta(days=1)

    # Weekly breakdown by day (current week, Mon-Sun)
    weekday_start = today - timedelta(days=today.weekday())  # Monday
    weekly = []
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i in range(7):
        d = weekday_start + timedelta(days=i)
        day_sessions = [s for s in sessions if s["date"] and
                        (s["date"].date() if hasattr(s["date"], "date") else s["date"]) == d]
        counts = defaultdict(int)
        for s in day_sessions:
            t = s["type"]
            if t in ("School", "Personal Project", "Grind"):
                counts[t] += 1
            else:
                counts["School"] += 1  # Default unknown to school
        weekly.append({
            "day": day_names[i],
            "school": counts.get("School", 0),
            "personal": counts.get("Personal Project", 0),
            "grind": counts.get("Grind", 0),
        })

    # By type totals
    type_counts = defaultdict(int)
    for s in sessions:
        t = s["type"]
        if t == "Personal Project":
            type_counts["personal"] += 1
        elif t == "Grind":
            type_counts["grind"] += 1
        else:
            type_counts["school"] += 1

    # Last 14 days heatmap
    last_14 = []
    for i in range(13, -1, -1):
        d = today - timedelta(days=i)
        count = sum(1 for s in sessions if s["date"] and
                    (s["date"].date() if hasattr(s["date"], "date") else s["date"]) == d)
        last_14.append(count)

    data = {
        "totalSessions": total_sessions,
        "avgRating": avg_rating,
        "flowStates": flow_states,
        "streak": streak,
        "weeklyByDay": weekly,
        "byType": {
            "school": type_counts.get("school", 0),
            "personal": type_counts.get("personal", 0),
            "grind": type_counts.get("grind", 0),
        },
        "last14Days": last_14,
        "lastUpdated": now.isoformat(),
    }

    with open("data.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"Processed {total_sessions} sessions. Streak: {streak} days. Avg rating: {avg_rating}")

if __name__ == "__main__":
    main()
