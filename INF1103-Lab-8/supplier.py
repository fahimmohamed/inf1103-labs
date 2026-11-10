class Supplier:
    """Represents ONE supplier. A Supplier exists on its own; Products only refer to it (association)."""

    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        if not isinstance(supplier_id, str) or not supplier_id.strip() or len(supplier_id.split()) > 1:
            raise ValueError("Supplier ID must be text without spaces.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Supplier name cannot be empty.")
        if not isinstance(contact_email, str) or "@" not in contact_email or " " in contact_email.strip():
            raise ValueError("Contact email must contain '@' and no spaces.")

        self.__supplier_id: str = supplier_id.strip()
        self.__name: str = name.strip()
        self.__contact_email: str = contact_email.strip()

    # ---------- getters (read-only access) ----------

    def get_supplier_id(self) -> str:
        return self.__supplier_id

    def get_name(self) -> str:
        return self.__name

    def get_contact_email(self) -> str:
        return self.__contact_email

    # ---------- display ----------

    def display_information(self) -> None:
        print(f"Supplier ID: {self.__supplier_id} | Name: {self.__name} | "
              f"Email: {self.__contact_email}")