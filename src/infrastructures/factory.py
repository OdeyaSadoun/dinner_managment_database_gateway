import os
from api.controllers.user_controller import UserController
from api.controllers.table_controller import TableController
from api.controllers.person_controller import PersonController
from api.routers.user_router import UserRouter
from api.routers.table_router import TableRouter
from api.routers.person_router import PersonRouter
from globals.consts.zmq_const_strings import ZMQConstStrings
from globals.consts.consts import Consts
from globals.consts.const_strings import ConstStrings
from models.managers.mongodb_database_manager import MongoDBDatabaseManager
from models.managers.zmq_server_manager import ZMQServerManager


class Factory:
    @staticmethod
    def create_database_manager():
        return MongoDBDatabaseManager()
    
    @staticmethod
    def create_person_router(database_manager):
        person_controller = PersonController(database_manager)
        return PersonRouter(ZMQConstStrings.person_resource, person_controller)
    
    @staticmethod
    def create_table_router(database_manager):
        table_controller = TableController(database_manager)
        return TableRouter(ZMQConstStrings.table_resource, table_controller)
    
    @staticmethod
    def create_user_router(database_manager):
        user_controller = UserController(database_manager)
        return UserRouter(ZMQConstStrings.auth_resource, user_controller)
    
    @staticmethod    
    def create_routers(database_manager):
        return [
            Factory.create_person_router(database_manager),
            Factory.create_table_router(database_manager),
            Factory.create_user_router(database_manager)
        ]
    
    @staticmethod
    def create_zmq_server(routers):
        return ZMQServerManager(routers, os.getenv(ConstStrings.localhost_env_key), int(os.getenv(ConstStrings.port_env_key)))
    
    # def create_test_guard_controller(database_manager):
    #     return TestGuardController(database_manager)

    # def create_test_real_people_controller(database_manager):
    #     return RealPeopleAssignmentDatabase(database_manager)

    # def create_test_real_guards_controller(database_manager):
    #     return RealGuardAssignmentDatabase(database_manager)
    
    # def create_test_guard_assignment_database(database_manager):
    #     return GuardAssignmentDatabase(database_manager)
    
    @staticmethod
    def create_all():
        database_manager = Factory.create_database_manager()
        # Factory.create_test_guard_assignment_database(database_manager)
        # Factory.create_test_real_people_controller(database_manager)
        # Factory.create_test_real_guards_controller(database_manager)
        routers = Factory.create_routers(database_manager)
        Factory.create_zmq_server(routers)