from database import Base
from sqlalchemy import Column, BigInteger, String, Float, ForeignKey
from sqlalchemy.orm import relationship


class Recipe(Base):
    __tablename__ = 'recipe'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=True)
    ingredients = relationship("Ingredient", back_populates="recipe")
    steps = relationship("Step", back_populates="recipe")


class Ingredient(Base):
    __tablename__ = 'ingredient'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=True)
    quantity = Column(Float, nullable=True)
    recipe_id = Column(BigInteger, ForeignKey('recipe.id'))
    recipe = relationship("Recipe", back_populates="ingredients")


class Step(Base):
    __tablename__ = 'step'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    text = Column(String(500), nullable=True)
    recipe_id = Column(BigInteger, ForeignKey('recipe.id'))
    recipe = relationship("Recipe", back_populates="steps")

