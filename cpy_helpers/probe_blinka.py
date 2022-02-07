# SPDX-FileCopyrightText: 2022 Tammy Cravit
#
# SPDX-License-Identifier: MIT

import usb.core
from usb.core import Device, USBError
import usb.util


class ProbeBlinka:
    """
    `probe_blinka`
    ==============

    The ProbeBlinka class helps you determine which Blinka interface module(s)
    are present on your system. It's used by the probe_blinka CLI command to
    find a suitable Blinka interface board.

    * Author: Tammy Cravit <tammy@tammymakesthings.com>
    """

    def __init__(self, preferred_board: str = 'u2if'):
        """
        Create an instance of the ProbeBlinka class.
        """

        self.preferred_board = preferred_board

    @staticmethod
    def is_usb_device_present(vendor_id: int, product_id: int) -> bool:
        """
        Checks if a specific USB device (with the given vendor_id and
        product_id) is present on the system.
        """

        try:
            device: Device = usb.core.find(
                idVendor=vendor_id,
                idProduct=product_id)
            if device is None:
                return False
        except USBError:
            return False
        return True

    @staticmethod
    def is_mcp2221_present() -> bool:
        """
        Check if an MCP2221 board is present on the system.
        """

        return ProbeBlinka.is_usb_device_present(vendor_id=0x04D8,
                                                 product_id=0x00DD)

    @staticmethod
    def is_ft232h_present() -> bool:
        """
        Check if an FT232H board is present on the system.
        """

        return ProbeBlinka.is_usb_device_present(vendor_id=0x0403,
                                                 product_id=0x6014)

    @staticmethod
    def is_rpi_u2if_present() -> bool:
        """
        Check if a Raspberry Pi Pico U2IF board is present on the system.
        """

        return ProbeBlinka.is_usb_device_present(vendor_id=0xCAFE,
                                                 product_id=0x4005)

    @staticmethod
    def probe_devices() -> dict:
        """
        Probe the system for all known Blinka-compatible boards. Returns
        a dict with a boolean indicating whether each kind of board is present
        on the system.
        """

        results: dict = {}
        results["mcp2221"] = ProbeBlinka.is_mcp2221_present()
        results["ft232h"] = ProbeBlinka.is_ft232h_present()
        results["u2if"] = ProbeBlinka.is_rpi_u2if_present()
        return results

    @staticmethod
    def available_boards() -> list:
        """
        Return a list of all the boards that are available on the system.
        """

        probe_results: dict = ProbeBlinka.probe_devices()
        available_boards: list = [
            k
            for k, v in probe_results.items()
            if v
        ]
        return available_boards

    def available_board(self) -> str:
        """
        Find an available Blinka board. If multiple boards are found, returns
        the preferred board (if it's present) or the first board found by the
        probe (if not). If no boards are found, returns None.
        """

        available_boards: list = ProbeBlinka.available_boards()
        if self.preferred_board in available_boards:
            return self.preferred_board
        if len(available_boards):
            return available_boards[0]
        return None
