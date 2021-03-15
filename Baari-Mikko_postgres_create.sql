CREATE TABLE "drinks" (
	"Id" serial NOT NULL,
	"drink" TEXT NOT NULL UNIQUE,
	CONSTRAINT "drinks_pk" PRIMARY KEY ("Id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "ingredients" (
	"id" serial NOT NULL,
	"ingredient" serial NOT NULL UNIQUE,
	CONSTRAINT "ingredients_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "recipes" (
	"drink_id" int NOT NULL,
	"ingredient_id" int NOT NULL,
	"quantity" int NOT NULL
) WITH (
  OIDS=FALSE
);



CREATE TABLE "pumps" (
	"id" serial NOT NULL,
	"ingredient_id" serial NOT NULL,
	CONSTRAINT "pumps_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "orders" (
	"user_id" int NOT NULL,
	"drink_id" int NOT NULL,
	"timestamp" TIMESTAMP NOT NULL
) WITH (
  OIDS=FALSE
);



CREATE TABLE "users" (
	"id" serial NOT NULL,
	"user" TEXT NOT NULL UNIQUE,
	"face" TEXT NOT NULL UNIQUE,
	"img" TEXT NOT NULL UNIQUE,
	"admin" BOOLEAN NOT NULL,
	CONSTRAINT "users_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);





ALTER TABLE "recipes" ADD CONSTRAINT "recipes_fk0" FOREIGN KEY ("drink_id") REFERENCES "drinks"("Id");
ALTER TABLE "recipes" ADD CONSTRAINT "recipes_fk1" FOREIGN KEY ("ingredient_id") REFERENCES "ingredients"("id");

ALTER TABLE "pumps" ADD CONSTRAINT "pumps_fk0" FOREIGN KEY ("ingredient_id") REFERENCES "ingredients"("id");

ALTER TABLE "orders" ADD CONSTRAINT "orders_fk0" FOREIGN KEY ("user_id") REFERENCES "users"("id");
ALTER TABLE "orders" ADD CONSTRAINT "orders_fk1" FOREIGN KEY ("drink_id") REFERENCES "drinks"("Id");


