# GiG
from typing import Type, TypeVar

from fastapi import HTTPException, status
from sqlmodel import Session, SQLModel

SQLModelType = TypeVar("SQLModelType", bound=SQLModel)


def create_entity(session: Session, entity: SQLModelType) -> SQLModelType:
    try:
        # Dynamically find the type of this object and validate it
        db_item = type(entity).model_validate(entity)
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error when processing {entity.__tablename__} {e}",
        ) from e
    return db_item


def get_entity(
    session: Session, entity_id: int, entity_type: Type[SQLModelType]
) -> SQLModelType:
    db_item = session.get(entity_type, entity_id)
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cannot find {entity_type.__tablename__} with ID {entity_id}",
        )
    return db_item


def update_entity(
    session: Session,
    entity_id: int,
    entity: SQLModelType,
) -> SQLModelType:
    db_item = session.get(type(entity), entity_id)
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item type {type(entity).__tablename__} with ID {entity_id} not found",
        )

    try:
        entity_data = entity.model_dump(exclude_unset=True)
        db_item.sqlmodel_update(entity_data)

        # Do not try to use the output of model_validate
        # as it will cause SQLModel errors when inserting
        _ = type(entity).model_validate(db_item)

        session.add(db_item)
        session.commit()
        session.refresh(db_item)
    except Exception as e:
        print(f"Got exception {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error when processing {type(entity).__tablename__} with ID {entity_id}: {e}",
        ) from e
    return db_item


def delete_entity(
    session: Session, entity_id: int, entity_type: Type[SQLModelType]
) -> dict:
    db_item = session.get(entity_type, entity_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entity {entity_type.__tablename__} with ID {entity_id} not found",
        )

    try:
        session.delete(db_item)
        session.commit()
        return {"ok": True}
    except Exception as e:
        print(f"Got exception {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error when processing {entity_type.__tablename__} with ID {entity_id}: {e}",
        ) from e
