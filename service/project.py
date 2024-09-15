from db_configs.db_settings import execute_query, fetchall
from db_configs.queries import insert_project, update_project_approval, update_project_rejection, \
    select_all_projects, select_all_approved_projects, select_all_rejected_projects


def create_project(category, name, description, budget, location):
    '''Creates a new project with the given details and sets approval status to False by default.'''
    try:
        print(location)
        execute_query(insert_project(), (category, name, description, budget, location, False))
        return 'Project created successfully!'
    except Exception as e:
        return {'error': str(e)}


def approve_project(project_id):
    '''Approves a project by updating its status to approved.'''
    try:
        execute_query(update_project_approval(), (project_id,))
        return 'Project approved!'
    except Exception as e:
        return {'error': str(e)}


def reject_project(project_id):
    '''Rejects a project by updating its status to rejected.'''
    try:
        execute_query(update_project_rejection(), (project_id,))
        return 'Project rejected!'
    except Exception as e:
        return {'error': str(e)}


def view_all_projects():
    '''Fetches and returns a list of all projects from the database.'''
    return fetchall(select_all_projects())


def view_all_approved_projects():
    '''Fetches and returns a list of all approved projects from the database.'''
    return fetchall(select_all_approved_projects())


def view_all_rejected_projects():
    '''Fetches and returns a list of all rejected projects from the database.'''
    return fetchall(select_all_rejected_projects())
