var QUEUE_DATA = [];

/*************************************************
 * Send update to the controller.
*************************************************/
// Aborts the active task, if there is one.
function queue_stop_current() {
    send_data({
        "request": "queue_stop_active"
    });
}

// Removes an unprocessed item from the queue.
function queue_drop_item(id) {
    send_data({
        "request": "queue_drop_item",
        "id": id
    });
}

// Removes all processed items from the queue.
function queue_clear() {
    send_data({
        "request": "queue_clear"
    });
}

/*************************************************
 * Received update from the controller.
*************************************************/
function update_queue_status(request) {
    // The active item status has changed (e.g. now installing). Updates the
    // lower-left queue status of the application.
    //
    // Variable         Example                 Description
    // ---------------- ----------------------- -----------------------------------
    // request          update_queue_status     Required
    // icon             ok                      Value either: "ok", "busy", "failed"
    // action_text      Installing Caja (1 of.. Display this text for the action.
    // details_text     app_progress            Display this text for the details. Optional, can be blank.
    // value            5                       Current value for progress bar. If -1, will pulsate.
    // value_end        10                      Total value for progress bar. If 0, will be hidden.
}

function update_queue_list(request) {
    // Items were added/removed/changed state in the queue. Updates the queue
    // page if it is open.
    //
    // Variable         Example                 Description
    // ---------------- ----------------------- -----------------------------------
    // request          update_queue_list       Required
    // queue            [{1..},{2..}]           Queue JSON data

    QUEUE_DATA = request;

    if (CURRENT_TAB === "queue") {
        _update_queue_view();
    }
}

/*************************************************
 * Internal view functions to update the page.
*************************************************/
function _update_queue_button() {
    //
    // Run when the queue length has changed.
    //
    var button_text = get_string("queue").replace("0", QUEUE_DATA.length);
    $("#tab-button-queue span").html(button_text);

    // TODO: Queue length should reflect pending tasks.
}
