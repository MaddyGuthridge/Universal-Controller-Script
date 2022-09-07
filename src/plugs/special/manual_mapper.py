"""
plugs > manual_mapper.py

Contains code used to manually map control surface events to CC events in the
case where said events aren't handled.

This mapping is done by taking a snapshot of available device controls and
then assigning each control an index which it will output.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
