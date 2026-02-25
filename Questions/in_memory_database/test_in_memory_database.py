import pytest
from simulation_solution import InMemoryDatabase
from simulation import Simulation
class TestLevel1:
    def test_set_and_get(self):
        db = InMemoryDatabase()
        assert db.set("user1", "name", "Alice") == ""
        assert db.set("user1", "age", "30") == ""
        assert db.get("user1", "name") == "Alice"
        assert db.get("user1", "age") == "30"

    def test_set_overwrite(self):
        db = InMemoryDatabase()
        assert db.set("user1", "name", "Alice") == ""
        assert db.set("user1", "name", "Bob") == ""
        assert db.get("user1", "name") == "Bob"

    def test_get_non_existent(self):
        db = InMemoryDatabase()
        assert db.get("user1", "field") == ""
        assert db.set("user1", "name", "Alice") == ""
        assert db.get("user1", "non_existent") == ""

    def test_delete(self):
        db = InMemoryDatabase()
        assert db.set("user1", "name", "Alice") == ""
        assert db.delete("user1", "name") == "true"
        assert db.get("user1", "name") == ""
        assert db.delete("user1", "name") == "false"
        assert db.delete("non_existent", "field") == "false"

class TestLevel2:
    def test_scan(self):
        db = InMemoryDatabase()
        assert db.set("user1", "name", "Alice") == ""
        assert db.set("user1", "age", "30") == ""
        assert db.set("user1", "city", "NY") == ""
        assert db.set("user1", "abc", "123") == ""
        assert db.scan("user1") == "abc(123), age(30), city(NY), name(Alice)"
        assert db.scan("non_existent") == ""

    def test_scan_by_prefix(self):
        db = InMemoryDatabase()
        assert db.set("user1", "name", "Alice") == ""
        assert db.set("user1", "age", "30") == ""
        assert db.set("user1", "city", "NY") == ""
        assert db.set("user1", "abc", "123") == ""
        assert db.scan_by_prefix("user1", "a") == "abc(123), age(30)"
        assert db.scan_by_prefix("user1", "n") == "name(Alice)"
        assert db.scan_by_prefix("user1", "xyz") == ""

class TestLevel3:
    def test_set_at_and_get_at(self):
        db = InMemoryDatabase()
        assert db.set_at("user1", "name", "Alice", timestamp=100) == ""
        assert db.set_at("user1", "age", "30", timestamp=101) == ""
        assert db.get_at("user1", "name", timestamp=102) == "Alice"
        assert db.get_at("user1", "age", timestamp=103) == "30"

    def test_set_at_and_get_at_non_existent(self):
        db = InMemoryDatabase()
        assert db.get_at("user2", "name", timestamp=100) == ""
        # Test that get_at returns empty string for non-existent field
        assert db.get_at("user1", "non_existent", timestamp=101) == ""

    def test_set_at_with_ttl_and_get_at(self):
        db = InMemoryDatabase()
        # The field is available between [100, 110)
        assert db.set_at_with_ttl("user1", "name", "Alice", timestamp=100, ttl=10) == ""
        # At timestamp 105, the field should still be available
        assert db.get_at("user1", "name", timestamp=105) == "Alice"
        # At timestamp 110, the field should have expired
        assert db.get_at("user1", "name", timestamp=110) == ""
        # At timestamp 115, the field should still be expired
        assert db.get_at("user1", "name", timestamp=115) == ""

    def test_set_at_with_ttl_overwrite_expiry(self):
        db = InMemoryDatabase()
        # Set a field with TTL
        assert db.set_at_with_ttl("user1", "name", "Alice", timestamp=100, ttl=10) == ""
        # Overwrite the same field without TTL
        assert db.set_at("user1", "name", "Bob", timestamp=105) == ""
        # The field should now return the new value and not expire
        assert db.get_at("user1", "name", timestamp=110) == "Bob"
        assert db.get_at("user1", "name", timestamp=120) == "Bob"

    def test_set_at_with_ttl_overwrite_expiry_2(self):
        db = InMemoryDatabase()
        # Set a field with TTL
        assert db.set_at_with_ttl("user1", "name", "Alice", timestamp=100, ttl=10) == ""
        # At timestamp 105, the field should still be available
        assert db.get_at("user1", "name", timestamp=105) == "Alice"
        # Overwrite the same field with a new TTL: [106, 116)
        assert db.set_at_with_ttl("user1", "name", "Bob", timestamp=106, ttl=10) == ""
        # The field should now return the new value and expire at timestamp 116
        assert db.get_at("user1", "name", timestamp=110) == "Bob"
        assert db.get_at("user1", "name", timestamp=117) == ""

    def test_set_at_with_ttl_and_get_all(self):
        db = InMemoryDatabase()
        # Set multiple fields with different TTLs
        # Field name "name" is available between [100, 110)
        assert db.set_at_with_ttl("user1", "name", "Alice", timestamp=100, ttl=10) == ""
        # Field name "age" is available between [101, 106)
        assert db.set_at_with_ttl("user1", "age", "30", timestamp=101, ttl=5) == ""
        # Field name "city" is available between [102, 117)
        assert db.set_at_with_ttl("user1", "city", "NY", timestamp=102, ttl=15) == ""

        assert db.get("user1", "name") == "Alice"
        assert db.get("user1", "age") == "30"
        assert db.get("user1", "city") == "NY"
class TestLevel4:
    pass