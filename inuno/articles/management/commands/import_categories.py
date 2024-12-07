import json
import os
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from ...models import Category, SubCategory


class Command(BaseCommand):
    help = "Import categories and subcategories from JSON file"

    def handle(self, *args, **kwargs):
        # Define the path to the JSON file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "categories.json")

        # Check if the file exists
        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        # Load the JSON data
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.stderr.write(self.style.ERROR(f"Error decoding JSON: {e}"))
            return

        # Validate the structure of the JSON file
        if "categories" not in data or not isinstance(data["categories"], list):
            self.stderr.write(
                self.style.ERROR(
                    "Invalid JSON structure: 'categories' key is missing or not a list"
                )
            )
            return

        # Process categories and subcategories
        for category_data in data["categories"]:
            category_name = category_data.get("name")
            subcategories = category_data.get("subcategories", [])

            if not category_name:
                self.stderr.write(
                    self.style.WARNING("Category name is missing; skipping entry")
                )
                continue

            # Check if the category exists
            category = Category.objects.filter(name=category_name).first()
            if category:
                self.stdout.write(
                    self.style.NOTICE(f"Skipping existing category: {category_name}")
                )
            else:
                # Create the category
                category = Category.objects.create(
                    name=category_name,
                    slug=self.generate_unique_slug(category_name, Category),
                )
                self.stdout.write(
                    self.style.SUCCESS(f"Created category: {category_name}")
                )

            # Process subcategories
            for subcategory_name in subcategories:
                if not subcategory_name:
                    self.stderr.write(
                        self.style.WARNING(
                            f"Subcategory name is missing for category '{category_name}'; skipping entry"
                        )
                    )
                    continue

                # Check if the subcategory exists
                subcategory = SubCategory.objects.filter(
                    parent=category, name=subcategory_name
                ).first()
                if subcategory:
                    self.stdout.write(
                        self.style.NOTICE(
                            f"  Skipping existing subcategory: {subcategory_name}"
                        )
                    )
                else:
                    # Create the subcategory
                    SubCategory.objects.create(
                        parent=category,
                        name=subcategory_name,
                        slug=self.generate_unique_slug(subcategory_name, SubCategory),
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f"  Created subcategory: {subcategory_name}")
                    )

        self.stdout.write(self.style.SUCCESS("Import completed successfully!"))

    @staticmethod
    def generate_unique_slug(name, model_class):
        """
        Generate a unique slug for a given name and model class.
        """
        base_slug = slugify(name)
        unique_slug = base_slug
        counter = 1

        # Ensure the slug is unique
        while model_class.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{base_slug}-{counter}"
            counter += 1

        return unique_slug
