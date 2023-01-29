/**
 * This file is part of the 1st Solidity Gas Golfing Contest.
 *
 * This work is licensed under Creative Commons Attribution ShareAlike 3.0.
 * https://creativecommons.org/licenses/by-sa/3.0/
 */

pragma solidity ^0.4.23;

contract IndexOf {
    /**
     * @dev Returns the index of the first occurrence of `needle` in `haystack`,
     *      or -1 if `needle` is not found in `haystack`.
     *
     * Input strings may be of any length <2^255.
     *
     * @param haystack The string to search.
     * @param needle The string to search for.
     * @return The index of `needle` in `haystack`, or -1 if not found.
     */
    function indexOf(string haystack, string needle) public pure returns(int) {
        // NOT OPTIMIZED!!! JUST TRYING TO GET THE TRUFFLE TO WORK

        bytes memory haystackBytes = bytes(haystack);
        bytes memory needleBytes = bytes(needle);

        uint256 needleLength = haystackBytes.length;
        uint256 needleIndex = 0;
        int256 index = -1;

        for(uint256 i = 0; i < haystackBytes.length; i++ ) {
            if (haystackBytes[i] == needleBytes[needleIndex]) {
                needleIndex++;
                if (needleIndex == needleLength){
                    index = int256(i - needleLength);
                    break;
                }
            }
        }

        return index;
    }
}

