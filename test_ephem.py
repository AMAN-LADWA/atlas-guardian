from agent.tools.jpl_horizons import get_ephemeris

rows = get_ephemeris(days=2)

for r in rows[:5]:
    print(r)
