from django.urls import path

from . import views

app_name = 'project'

urlpatterns = [
    # main page
    path('', views.index, name='index'),
    # page where all projects are listed
    path('projects/', views.projects, name='projects'),
    # page to add a new project
    path('add_project/', views.add_project, name='add_project'),
    # detail page for a specific   project
    path('projects/<int:pk>/', views.project, name='project'),
    # page to edit an existing project
    path('projects/<int:pk>/edit/', views.edit_project, name='edit_project'),
    # page to delete a  project
    path('projects/<int:pk>/delete/', views.delete_project, name='delete_project'),
    # search project
    path('search_project/', views.search_projects, name='search_projects'),
    # add a todolist in a project
    path('projects/<int:project_id>/add_todolist/', views.add_todolist, name='add_todolist'),
    # see a detail for a specific todolist
    path('projects/<int:project_id>/todolist/<int:pk>/', views.todolist, name='todolist'),
    # edit a todolist
    path('projects/<int:project_id>/todolist/<int:pk>/edit_todolist/', views.edit_todolist, name='edit_todolist'),
    # delete a project
    path('projects/<int:project_id>/todolist/<int:pk>/delete_todolist/', views.delete_todolist, name='delete_todolist'),
    # add a task
    path('projects/<int:project_id>/todolist/<int:todolist_id>/add_task/', views.add_task, name='add_task'),
    # detail for  task
    path('projects/<int:project_id>/todolist/<int:todolist_id>/<int:task_id>/detail/', views.task_detail,
         name='task_detail'),
    # edit a task
    path('projects/<int:project_id>/todolist/<int:todolist_id>/<int:task_id>/edit_task/', views.edit_task,
         name='edit_task'),
    # delete a task
    path('projects/<int:project_id>/todolist/<int:todolist_id>/<int:task_id>/delete_task/', views.delete_task,
         name='delete_task'),
    # remove a task material resource
    path('projects/<int:project_id>/todolist/<int:todolist_id>/<int:task_id>/<int:material_id>/delete/',
         views.delete_task_material, name='delete_task_material'),
    # remove a task team
    path('projects/<int:project_id>/todolist/<int:todolist_id>/<int:task_id>/<int:team_id>/delete_team/',
         views.delete_task_team, name='delete_task_team'),

    # url to see  agents
    path('agents/', views.agents, name='agents'),
    # add agent
    path('add_agent/', views.add_agent, name='add_agent'),
    # edit agent
    path('agents/<int:pk>/edit/', views.edit_agent, name='edit_agent'),
    # delete agent
    path('agents/<int:pk>/delete/', views.delete_agent, name='delete_agent'),
    # search an agent
    path('search/', views.search_agents, name='search_agents'),
    # url to see  teams
    path('teams/', views.teams, name='teams'),
    path('search/', views.search_teams, name='search_teams'),
    # add a team
    path('add_team/', views.add_team, name='add_team'),
    # team details
    path('teams/<int:team_id>/', views.team_details, name='team_details'),
    # edit team
    path('teams/<int:team_id>/edit/', views.edit_team, name='edit_team'),
    # delete team
    path('teams/<int:team_id>/delete/', views.delete_team, name='delete_team'),
    # delete a team member
    path('teams/<int:team_id>/<int:member_id>/delete', views.delete_team_member, name='delete_team_member'),
    # list materials resources
    path('materials/', views.materials, name='materials'),
    # add material
    path('add_material/', views.add_material, name='add_material'),
    # edit material
    path('materials/<int:material_id>/edit', views.edit_material, name='edit_material'),
    # delete material
    path('materials/<int:material_id>/delete', views.delete_material, name='delete_material'),
    # list softwares
    path('softwares/', views.softwares, name='softwares'),
    # add a software
    path('add_software/', views.add_software, name='add_software'),
    # edit a specific software
    path('softwares/<int:software_id>/edit', views.edit_software, name='edit_software'),
    # delete a software
    path('softwares/<int:software_id>/delete', views.delete_software, name='delete_software'),
    # search software
    path('search_software/', views.search_software, name='search_software'),
    # list reunions
    path('projects/<int:project_id>/todolist/<int:todolist_id>/<int:task_id>/detail/reunions', views.reunions,
         name='reunions'),
    # add reunion
    path('projects/<int:project_id>/todolist/<int:todolist_id>/<int:task_id>/detail/reunions/add_reunion',
         views.add_reunion, name='add_reunion'),
    # reunion detail
    path('projects/<int:project_id>/todolist/<int:todolist_id>/<int:task_id>/detail/reunions/<int:reunion_id>/',
         views.reunion_detail, name='reunion_detail'),
    # edit a reunion
    path('projects/<int:project_id>/todolist/<int:todolist_id>/<int:task_id>/detail/reunions/<int:reunion_id>/edit/',
         views.edit_reunion, name='edit_reunion'),
    # delete reunion
    path('projects/<int:project_id>/todolist/<int:todolist_id>/<int:task_id>/detail/reunions/<int:reunion_id>/delete',
         views.delete_reunion, name='delete_reunion'),

    # create a repport for reunion
    path('projects/<int:project_id>/todolist/<int:todolist_id>/<int:task_id>/detail/reunions/<int:reunion_id>/create_report/',
        views.create_report, name='create_report'),
    # report detail
    path('projects/<int:project_id>/todolist/<int:todolist_id>/<int:task_id>/detail/reunions/<int:reunion_id>/<int:report_id>/',
         views.report_detail, name='report_detail'),
    # delete report
    path('projects/<int:project_id>/todolist/<int:todolist_id>/<int:task_id>/detail/reunions/<int:reunion_id>/<int:report_id>/delete/',
         views.delete_report, name='delete_report'),
    # edit a report
    path('projects/<int:project_id>/todolist/<int:todolist_id>/<int:task_id>/detail/reunions/<int:reunion_id>/<int:report_id>/edit/',
         views.edit_report, name='edit_report'),
    # add a product to task
    path('projects/<int:project_id>/todolist/<int:todolist_id>/<int:task_id>/detail/', views.add_product,
         name='add_product'),
]
