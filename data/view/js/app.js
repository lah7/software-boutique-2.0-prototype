/*************************************************
 * Send request to the controller.
*************************************************/
// Start an application (from queue or app details page)
function launch_app_id(id) {
    send_data({
        "request": "app_launch",
        "id": id
    });
}

// View error details for a failed item in the queue.
function view_error_app_id(id) {
    send_data({
        "request": "app_show_error",
        "id": id
    });
}

/*************************************************
 * Received update from the controller.
*************************************************/


/*************************************************
 * Internal view functions to update the page.
*************************************************/
