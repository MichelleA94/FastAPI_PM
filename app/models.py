from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

from .database import Base

class Event(Base):
    __tablename__ = "eventdata"

    id = Column(Integer, primary_key=True, nullable=False)
    created_at =  Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    app_id =  Column(Integer, ForeignKey("platforms.id", ondelete="CASCADE"), nullable=False)
    customer_id =  Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    instance_id =  Column(Integer, ForeignKey("instances.id", ondelete="CASCADE"), nullable=False)
    queue_id =  Column(Integer, ForeignKey("queues.id", ondelete="CASCADE"), nullable=False)
    script_id =  Column(Integer, ForeignKey("scripts.id", ondelete="CASCADE"), nullable=False)
    endpoint =  Column(String, nullable=False)
    contact_id =  Column(String, nullable=True)
    integration_id =  Column(Integer, ForeignKey("integrations.id", ondelete="CASCADE"), nullable=False)
    severity_id =  Column(Integer, ForeignKey("severities.id", ondelete="CASCADE"), nullable=False)
    response_id =  Column(Integer, ForeignKey("responsecodes.id", ondelete="CASCADE"), nullable=False)
    url =  Column(String, nullable=True)
    error =  Column(String, nullable=True)
    error_description =  Column(String, nullable=True)
    modality =  Column(Integer, ForeignKey("modality.id", ondelete="CASCADE"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")
 
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    created_at =  Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    username = Column(String, nullable=False, unique = True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

class Platform(Base):
    __tablename__ = "platforms"

    id = Column(Integer, primary_key=True, nullable=False)
    created_at =  Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    app_id = Column(String, nullable=False, unique = True)
    name = Column(String, nullable=False)

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, nullable=False)
    created_at =  Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    customer_id = Column(Integer, nullable=False, unique = True)
    customer_name = Column(String, nullable=False)

class Instance(Base):
    __tablename__ = "instances"

    id = Column(Integer, primary_key=True, nullable=False)
    created_at =  Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    cloud_region = Column(String, nullable=False)
    service_id = Column(String, nullable=False, unique = True)

class Queue(Base):
    __tablename__ = "queues"

    id = Column(Integer, primary_key=True, nullable=False)
    created_at =  Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    queue_id = Column(String, nullable=False)
    queue_name = Column(String, nullable=False)

class Script(Base):
    __tablename__ = "scripts"

    id = Column(Integer, primary_key=True, nullable=False)
    created_at =  Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    script_id = Column(String, nullable=False)
    script_type = Column(String, nullable=False)
    script_name = Column(String, nullable=False)

class Integration(Base):
    __tablename__ = "integrations"

    id = Column(Integer, primary_key=True, nullable=False)
    created_at =  Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    integration_name = Column(String, nullable=False)

class Severity(Base):
    __tablename__ = "severities"

    id = Column(Integer, primary_key=True, nullable=False)
    created_at =  Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    severity = Column(String, nullable=False)

class ResponseCode(Base):
    __tablename__ = "responsecodes"

    id = Column(Integer, primary_key=True, nullable=False)
    created_at =  Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    response_code = Column(Integer, nullable=False, unique = True)
    response_description = Column(String, nullable=False)

class Modality(Base):
    __tablename__ = "modality"

    id = Column(Integer, primary_key=True, nullable=False)
    created_at =  Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    modality = Column(String, nullable=False)


