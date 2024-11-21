from constanta import BASE_URL

class TestBookings:

    def test_positive_create_booking(self, booking_data, auth_session):
        """"Создание нового бронирования"""
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200
        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "ид букинга не найден в ответе"

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200

        booking_data_response = get_booking.json()
        assert booking_data_response['firstname'] == booking_data['firstname'], "Имя не совпадает с заданным"
        assert booking_data_response['lastname'] == booking_data['lastname'], "Фамилия не совпадает с заданным"
        assert booking_data_response['totalprice'] == booking_data['totalprice'], "Цена не совпадает с заданным"
        assert booking_data_response['depositpaid'] == booking_data['depositpaid'], "Статус не совпадает с заданным"
        assert booking_data_response['bookingdates']['checkin'] == booking_data['bookingdates']['checkin'], "Дата заезда не совпадает с заданным"
        assert booking_data_response['bookingdates']['checkout'] == booking_data['bookingdates']['checkout'], "Дата выезда не совпадает с заданным"

        delete_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert delete_booking.status_code == 201, f"Ошибка при удалении букинка с ид {booking_id}"

        get_deleted_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_deleted_booking.status_code == 404, "Букинг не был удален"

    def test_positive_post_without_required_field(self, auth_session, booking_data_field_is_empty):
        """Проверка обязательных полей"""
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data_field_is_empty)
        assert create_booking.status_code == 500

    def test_positive_put_object_booking(self, auth_session, booking_data):
        """"Обновление бронирования"""
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200
        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "ID booking not found"

        get_booking = auth_session.get(f"{BASE_URL}/booking", json=booking_data)
        assert get_booking.status_code == 200

        booking_data["firstname"] = "Иван"
        booking_data["lastname"] = "Иванов"
        booking_data["totalprice"] = 500
        booking_data["depositpaid"] = False
        booking_data["additionalneeds"] = "Breakfast111"
        booking_data["bookingdates"]["checkin"] = "2022-01-01"
        booking_data["bookingdates"]["checkout"] = "2022-01-03"

        put_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=booking_data)
        assert put_booking.status_code == 200

        updated_obj = put_booking.json()
        assert updated_obj["firstname"] == booking_data["firstname"]
        assert updated_obj["lastname"] == booking_data["lastname"]
        assert updated_obj["totalprice"] == booking_data["totalprice"]
        assert updated_obj["depositpaid"] == booking_data["depositpaid"]
        assert updated_obj["additionalneeds"] == booking_data["additionalneeds"]
        assert updated_obj["bookingdates"]["checkin"] == booking_data["bookingdates"]["checkin"]
        assert updated_obj["bookingdates"]["checkout"] == booking_data["bookingdates"]["checkout"]

        delete_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert delete_booking.status_code == 201, f"Ошибка при удалении букинга с ID {booking_id}"

        get_deleted_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_deleted_booking.status_code == 404, "Букинг не был удален"

    def test_positive_put_without_required_field_firstname(self, booking_data, auth_session):
        """"Проверка обязательных полей"""
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200
        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "ID booking not found"

        get_booking = auth_session.get(f"{BASE_URL}/booking", json=booking_data)
        assert get_booking.status_code == 200

        booking_data["firstname"] = None
        booking_data["lastname"] = "Иванов"
        booking_data["totalprice"] = 500
        booking_data["depositpaid"] = False
        booking_data["additionalneeds"] = "Breakfast111"
        booking_data["bookingdates"]["checkin"] = "2022-01-01"
        booking_data["bookingdates"]["checkout"] = "2022-01-03"

        put_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=booking_data)
        assert put_booking.status_code == 400

        delete_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert delete_booking.status_code == 201, f"Ошибка при удалении букинга с ID {booking_id}"

        get_deleted_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_deleted_booking.status_code == 404, "Букинг не был удален"

    def test_positive_put_object_update_deleted_booking(self, auth_session, booking_data):
        """"Проверка обновления несуществующего бронирования"""
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200
        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "ID booking not found"

        get_booking = auth_session.get(f"{BASE_URL}/booking", json=booking_data)
        assert get_booking.status_code == 200

        delete_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert delete_booking.status_code == 201, f"Ошибка при удалении букинга с ID {booking_id}"

        get_deleted_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_deleted_booking.status_code == 404, "Букинг не был удален"

        booking_data["firstname"] = "Иван"
        booking_data["lastname"] = "Иванов"
        booking_data["totalprice"] = 500
        booking_data["depositpaid"] = False
        booking_data["additionalneeds"] = "Breakfast111"
        booking_data["bookingdates"]["checkin"] = "2022-01-01"
        booking_data["bookingdates"]["checkout"] = "2022-01-03"

        put_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=booking_data)
        assert put_booking.status_code == 405

    def test_positive_patch_fields_booking(self, auth_session, booking_data):
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200
        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "ид букинга не найден в ответе"

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200

        patch_booking = auth_session.patch(f"{BASE_URL}/booking/{booking_id}", json=booking_data)
        assert patch_booking.status_code == 200

        updated_obj = patch_booking.json()
        assert updated_obj["firstname"] == booking_data["firstname"]
        assert updated_obj["lastname"] == booking_data["lastname"]

        delete_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert delete_booking.status_code == 201, f"Ошибка при удалении букинга с ID {booking_id}"

        get_deleted_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_deleted_booking.status_code == 404, "Букинг не был удален"







