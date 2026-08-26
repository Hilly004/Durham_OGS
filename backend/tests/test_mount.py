import socket
from unittest.mock import MagicMock

import pytest

from Hardware.Connections.Mount_Connection import MountConnection


def test_send_receive_sends_command_and_returns_response():

    connection = MountConnection(
        "127.0.0.1",
        3490
    )

    fake_socket = MagicMock()

    fake_socket.recv.return_value = (
        b"10micron GM2000HPS#"
    )

    connection.socket = fake_socket
    connection.connected = True


    response = connection.send_receive(
        ":GVP#",
        "#"
    )


    fake_socket.sendall.assert_called_once_with(
        b":GVP#"
    )

    assert response == (
        "10micron GM2000HPS#"
    )


def test_send_receive_disconnects_on_timeout():

    connection = MountConnection(
        "127.0.0.1",
        3490
    )

    fake_socket = MagicMock()

    fake_socket.recv.side_effect = (
        socket.timeout()
    )

    connection.socket = fake_socket
    connection.connected = True


    with pytest.raises(TimeoutError):

        connection.send_receive(
            ":GVP#",
            "#"
        )


    assert connection.connected is False
    assert connection.socket is None