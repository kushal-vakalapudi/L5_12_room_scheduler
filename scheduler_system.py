"""Book conference rooms and allocate shared equipment."""

from collections import Counter
import json
import sys
from datetime import datetime
from itertools import count

reservations = {}
equipment_pool = {"projector": 2, "microphone": 4, "webcam": 1}
conflicts = []
reservation_ids = count(1)


def schedule_room(room_id, time_slot, equipment_list=None):
    """Reserve a room for a valid same-day slot and optional equipment."""
    slot_hours(time_slot)
    if equipment_list is None:
        equipment_list = []

    requested_equipment = Counter(equipment_list)
    for equipment, quantity in requested_equipment.items():
        if equipment not in equipment_pool:
            raise ValueError(f"Unknown equipment: {equipment}")
        if equipment_pool[equipment] < quantity:
            raise ValueError(f"Not enough equipment available: {equipment}")

    for reservation in reservations.values():
        if (
            reservation["room"] == room_id
            and reservation["slot"] == time_slot
        ):
            conflicts.append(f"{room_id} double-booked at {time_slot}")

    for equipment, quantity in requested_equipment.items():
        equipment_pool[equipment] -= quantity

    reservation_id = next(reservation_ids)
    reservations[reservation_id] = {
        "room": room_id,
        "slot": time_slot,
        "equipment": equipment_list,
    }
    return reservation_id


def cancel_reservation(reservation_id):
    """Cancel a reservation and return its equipment to the pool."""
    reservation = reservations.get(reservation_id)
    if reservation is None:
        print(f"Reservation {reservation_id} not found.")
        return

    for equipment in reservation["equipment"]:
        equipment_pool[equipment] += 1
    del reservations[reservation_id]


def slot_hours(time_slot):
    """Return duration in hours for a valid same-day ``start-end`` slot."""
    parts = time_slot.split("-")
    if len(parts) != 2 or not all(part.isdigit() for part in parts):
        raise ValueError("slot must use the start-end hour format")

    start, end = (int(part) for part in parts)
    if not 0 <= start <= 23 or not 0 <= end <= 23:
        raise ValueError("slot hours must be between 0 and 23")
    if end <= start:
        raise ValueError("slot end must be later than its start")
    return end - start


def export_schedule(file="schedule.json"):
    """Write all reservations to a UTF-8 JSON file."""
    with open(file, "w", encoding="utf-8") as schedule_file:
        json.dump(reservations, schedule_file)


def log_conflicts(file="conflicts.log"):
    """Append conflicts to a log and display its contents."""
    try:
        with open(file, "a", encoding="utf-8") as conflict_file:
            for conflict in conflicts:
                conflict_file.write(f"{datetime.now()} {conflict}\n")
        with open(file, "r", encoding="utf-8") as conflict_file:
            print(conflict_file.read(), end="")
    except OSError as error:
        print(
            f"Unable to process conflict log ({type(error).__name__}).",
            file=sys.stderr,
        )


def main():
    """Run a short demonstration of room scheduling."""
    schedule_room("Board-1", "09-11")
    schedule_room("Board-1", "09-11")
    reservation_id = schedule_room("Huddle-3", "12-14")
    print(
        "Slot length for reservation:",
        slot_hours(reservations[reservation_id]["slot"]),
    )
    cancel_reservation(77)
    slot = input("Slot for Board-2, like 10-12 (Enter for 10-12): ") or "10-12"
    try:
        schedule_room("Board-2", slot, ["projector", "webcam"])
    except ValueError as error:
        print(f"Invalid slot: {error}", file=sys.stderr)
    export_schedule()
    log_conflicts()
    print("Equipment left:", equipment_pool)
    print("Reservations:", reservations)


if __name__ == "__main__":
    main()
