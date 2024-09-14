from db_configs.db_settings import execute_query, fetchall
from db_configs.queries import insert_project, update_project_approval, update_project_rejection, select_all_projects, \
    select_all_approved_projects, select_all_rejected_projects


def create_project(category, name, description, budget, location):
    try:
        print(location)
        execute_query(insert_project(), (category, name, description, budget, location, False))
        return {'message': 'Project created successfully!'}
    except Exception as e:
        return {'error': str(e)}


def approve_project(project_id):
    try:
        execute_query(update_project_approval(), (project_id,))
        return {'message': 'Project approved!'}
    except Exception as e:
        return {'error': str(e)}


def reject_project(project_id):
    try:
        execute_query(update_project_rejection(), (project_id,))
        return {'message': 'Project rejected!'}
    except Exception as e:
        return {'error': str(e)}


def view_all_projects():
    return fetchall(select_all_projects())


def view_all_approved_projects():
    return fetchall(select_all_approved_projects())


def view_all_rejected_projects():
    return fetchall(select_all_rejected_projects())
