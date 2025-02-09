// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleStorage {
    // State variable to store a string
    string private storedData;

    // Event to emit when data is changed
    event DataUpdated(string newValue);

    // Function to set a new value
    function set(string memory _data) public {
        storedData = _data;
        emit DataUpdated(_data);
    }

    // Function to retrieve the stored value
    function get() public view returns (string memory) {
        return storedData;
    }
}
