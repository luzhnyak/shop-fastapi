from typing import List, Optional

from sqlalchemy import (
    String,
    Integer,
    Boolean,
    ForeignKey,
    Text,
    Float,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.db import Base
from app.models.base_model import BaseModel


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=False, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"))

    parent: Mapped[Optional["Category"]] = relationship(remote_side=[id])
    products: Mapped[List["Product"]] = relationship(back_populates="category")


class Product(BaseModel):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=False, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    base_price: Mapped[float] = mapped_column(Float, nullable=False)
    sku: Mapped[str] = mapped_column(String, unique=True)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0)

    category: Mapped["Category"] = relationship(back_populates="products")
    options: Mapped[List["ProductOption"]] = relationship(back_populates="product")
    images: Mapped[List["ProductImage"]] = relationship(back_populates="product")
    order_items: Mapped[List["OrderItem"]] = relationship(back_populates="product")  # type: ignore
    reviews: Mapped[List["Review"]] = relationship(back_populates="product")  # type: ignore
    wishlist: Mapped[List["Wishlist"]] = relationship(back_populates="product")  # type: ignore


class ProductOption(Base):
    __tablename__ = "product_options"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    value: Mapped[str] = mapped_column(String, nullable=False)
    additional_price: Mapped[Optional[float]] = mapped_column(Float, default=0)

    product: Mapped["Product"] = relationship(back_populates="options")


class ProductImage(Base):
    __tablename__ = "product_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    image_url: Mapped[str] = mapped_column(String, nullable=False)
    is_main: Mapped[bool] = mapped_column(Boolean, default=False)

    product: Mapped["Product"] = relationship(back_populates="images")
