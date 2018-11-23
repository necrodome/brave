import time, pytest, inspect
from utils import *


def test_outputs(run_brave):
    run_brave()
    check_brave_is_running()
    assert_outputs([])

    # Create output, ignore attempts to set an ID
    add_output({'type': 'local', 'id': 99})
    assert_outputs([{'type': 'local', 'id': 0}])

    # Different types of outputs work:
    add_output({'type': 'image'})
    time.sleep(1)
    assert_outputs([{'type': 'local', 'id': 0}, {'type': 'image', 'id': 1}])

    # Change state to PAUSED
    update_output(1, {'state': 'NULL'})
    assert_outputs([{'type': 'local', 'id': 0}, {'type': 'image', 'id': 1, 'state': 'NULL'}], check_playing_state=False)

    # Change state to READY
    update_output(1, {'state': 'READY'})
    assert_outputs([{'type': 'local', 'id': 0}, {'type': 'image', 'id': 1, 'state': 'READY'}], check_playing_state=False)

    # Change state to NULL
    update_output(1, {'state': 'PAUSED'})
    assert_outputs([{'type': 'local', 'id': 0}, {'type': 'image', 'id': 1, 'state': 'PAUSED'}], check_playing_state=False)

    # Change state to PLAYING
    update_output(1, {'state': 'PLAYING'})
    time.sleep(1)
    assert_outputs([{'type': 'local', 'id': 0}, {'type': 'image', 'id': 1}])

    # TODO outputs need to support being updated
    # # Add a property to existing output
    # update_output(1, {'props': {'update_frequency': 5}})
    # assert_outputs([{'type': 'image', 'id': 1, 'props': {'update_frequency': 5}}])

    # Add a bad property to existing output
    update_output(1, {'props': {'not_real': 100}}, 400)
    assert_outputs([{'type': 'local', 'id': 0}, {'type': 'image', 'id': 1}])

    # Add a property to missing output
    update_output(4, {'props': {'update_frequency': 5}}, 400)

    # Removing an existing output works:
    delete_output(0)
    assert_outputs([{'type': 'image', 'id': 1}])

    # Removing a non-existant output causes a user error
    delete_output(3, expected_status_code=400) # Does not exist
    assert_outputs([{'type': 'image', 'id': 1}])
