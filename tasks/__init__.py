"""
Tasks package
-------------
Factory functions for each pipeline task in the DreamTeam agency.

Each factory accepts the relevant agent instance so that the same task
definition can be reused with different agent configurations.

Usage:
    from tasks.analysis import create_analysis_task
    task = create_analysis_task(architect_agent)
"""
