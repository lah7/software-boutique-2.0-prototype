// QUEUE_DATA - the controller sends data in this format:
//  [
//      {
//          "id": "app1"                // Unique ID of item (backend parameter)
//          "name": "Application 1"     // Name of application
//          "icon": "/path/to/img"      // Path to the icon
//          "action": "install"         // Either: 'install', 'remove'
//          "state": "processing"       // Either: 'pending', 'processing', 'processed'
//          "success": true             // Success or failed? Only applicable for 'processed' state.
//      }
//  ]

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

// Adds a new item to the queue.
function queue_add_item(backend, operation, app_id) {
    send_data({
        "request": "queue_add_item",
        "backend": backend,             // Either: 'snapd', 'apt', 'index'
        "operation": operation,         // Either: 'install', 'remove'
        "id": id                        // App name / package name / or index ID, depending on backend parameter.
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
function update_queue_status(data) {
    // Provides status updates for the active item (e.g. installation % complete).
    // Updates the lower-left of the application and 'in progress' heading on queue page.
    //
    // Variable         Example                 Description
    // ---------------- ----------------------- -----------------------------------
    // request          update_queue_status     Required
    // state            ok                      Value either: "ok", "busy", "error"
    // action_text      Installing Caja (1 of.. Display this text for the action.
    // details_text     app_progress            Display this text for the details. Optional, can be blank.
    // value            5                       Current value for progress bar. If -1, will pulsate.
    // value_end        10                      Total value for progress bar. If 0, will be hidden.

    _update_queue_status(data.state, data.action_text, data.details_text, data.value, data.value_end);
}

function update_queue_list(data) {
    // Items were added/removed/changed state in the queue. Updates the queue
    // page if it is open.
    //
    // Variable         Example                 Description
    // ---------------- ----------------------- -----------------------------------
    // request          update_queue_list       Required
    // queue            [{..},{..}]             Queue JSON data (see "QUEUE_DATA")

    QUEUE_DATA = data.queue;

    _update_queue_button();
    if (CURRENT_TAB === "queue") {
        _set_page_queue();
    }
}

/*************************************************
 * Internal view functions to update the page.
*************************************************/
function _set_page_queue() {
    var html_buffer_processing = [];
    var html_buffer_processed = [];
    var html_buffer_pending = [];

    for (i = 0; i < QUEUE_DATA.length; i++) {
        var item = QUEUE_DATA[i];
        var html_app_data = `<img class="app-icon" src="${item.icon}"/>
            <div class="app-name">${item.name}</div>`;
        var html_remove_button = `<a class="queue-remove" onclick="queue_drop_item('${item.id}')">${get_svg("fa-x")}</a>`;

        switch (item.state) {
            case "processing":
                var cur_value = $("#progress-bar").attr("value");
                var cur_total = $("#progress-bar").attr("total");
                html_buffer_processing.push(`
                    <div class="app-progress processing">
                        ${html_app_data}
                        <progress class="active-item-progress" value="${cur_value}" max="${cur_total}"></progress>
                        <div class="status busy">${get_svg("loading")}</div>
                        ${html_remove_button}
                    </div>
                `);
                break;

            case "processed":
                var status_text;
                var status_icon;
                var status_buttons;

                if (item.action === "install" && item.success === true) {
                    status_icon = get_svg("fa-check-circle");
                    status_text = get_string("queue_list_success_install");
                    status_buttons = `<button onclick="launch_app_id('${item.id}')">${get_svg("fa-external-link-alt")} ${get_string('launch')}</button>`
                    status_class = "install-success";
                }

                if (item.action === "remove" && item.success === true) {
                    status_icon = get_svg("fa-check-circle");
                    status_text = get_string("queue_list_success_remove");
                    status_buttons = "";
                    status_class = "remove-success";
                }

                if (item.action === "install" && item.success === false) {
                    status_icon = get_svg("fa-exclamation-triangle");
                    status_text = get_string("queue_list_failed_install");
                    status_buttons = `<button onclick="view_error_app_id('${item.id}')">${get_string("view_details")}</button>`
                    status_class = "install-failed";
                }

                if (item.action === "remove" && item.success === false) {
                    status_icon = get_svg("fa-exclamation-triangle");
                    status_text = get_string("queue_list_failed_remove");
                    status_buttons = `<button onclick="view_error_app_id('${item.id}')">${get_string("view_details")}</button>`
                    status_class = "remove-failed";
                }

                // For successful installations, just show the launch button.
                if (item.action === "install" && item.success === true) {
                    html_buffer_processed.push(`
                        <div class="app-progress processed ${status_class}">
                            ${html_app_data}
                            ${status_buttons}
                            ${html_remove_button}
                        </div>
                    `);
                } else {
                    html_buffer_processed.push(`
                        <div class="app-progress processed ${status_class}">
                            ${html_app_data}
                            <div class="status">${status_icon}</div>
                            <div class="status-text">${status_text}</div>
                            ${status_buttons}
                            ${html_remove_button}
                        </div>
                    `);
                }
                break;

            case "pending":
                if (item.action === "install") {
                    status_text = get_string("queue_list_pending_install");
                } else if (item.action === "remove") {
                    status_text = get_string("queue_list_pending_remove");
                }

                html_buffer_pending.push(`
                    <div class="app-progress pending">
                        ${html_app_data}
                        <div class="status-text">${status_text}</div>
                        <div class="status busy">${get_svg("loading")}</div>
                        ${html_remove_button}
                    </div>
                `);
                break;
        }
    }

    if (QUEUE_DATA.length === 0) {
        // Inform user about the queue page.
        $("content").html(`
            <div class="queue-page">
                <empty>
                    ${get_svg("fa-clone")}
                    <span>${get_string("queue_list_empty")}</span>
                </empty>
            </div>
        `);

    } else {
        // Show list of active/completed/queued tasks.
        var buffer = [`<div class="queue-page">`];

        buffer.push(`
            <div class="queue-toolbar">
                <button onclick="queue_clear()">${get_string("queue_list_clear")}</button>
            </div>`);

            if (html_buffer_processing.length > 0) {
                buffer.push(`<h2>${get_string("queue_list_title_processing")}</h2>`);
                buffer.push(html_buffer_processing.join(""));
            }

            if (html_buffer_pending.length > 0) {
                buffer.push(`<h2>${get_string("queue_list_title_pending")}</h2>`);
                buffer.push(html_buffer_pending.join(""));
            }

            if (html_buffer_processed.length > 0) {
                buffer.push(`<h2>${get_string("queue_list_title_processed")}</h2>`);
                buffer.push(html_buffer_processed.join(""));
            }

        buffer.push(`</div>`);
        $("content").html(buffer.join(""));

    }
}

function _update_queue_button() {
    //
    // Run when the queue length has changed.
    //
    var button_text = get_string("queue").replace("0", QUEUE_DATA.length);
    $("#tab-button-queue span").html(button_text);

    // TODO: Queue length should reflect pending tasks.
}

function _update_queue_status(icon, action_text, details_text, value, value_end) {
    // See update_queue_status() for parameters.

    var old_action_text = $("#progress-text").html();

    if (old_action_text !== action_text) {
        $("#footer-status").removeClass();
    }

    switch(icon) {
        case "ok":
            svg_name = "fa-check-circle";
            break;
        case "busy":
            svg_name = "loading";
            break;
        case "error":
            svg_name = "fa-exclamation-triangle";
            break;
        default:
            break;
    }

    $("#status-icon").html(get_svg(svg_name));
    $("#status-icon").removeClass().addClass(icon);

    if (action_text.length > 0) {
        $("#progress-text").html(action_text);
    }

    if (details_text.length > 0) {
        $("#progress-subtext").show().html(details_text);
    } else {
        $("#progress-subtext").hide().html(" ");
    }

    if (value === -1) {
        // Pulsating
        $("#progress-bar").removeAttr("value");
        $("#progress-bar").removeAttr("max");
        $(".active-item-progress").removeAttr("value");
        $(".active-item-progress").removeAttr("max");
    } else {
        $("#progress-bar").attr("value", value);
        $("#progress-bar").attr("max", value_end);
        $(".active-item-progress").attr("value", value);
        $(".active-item-progress").attr("max", value_end);
    }

    if (value_end === -1) {
        $("#progress-bar").hide();
    } else {
        $("#progress-bar").show();
    }

    // Only 'fade' if action text changes.
    if (old_action_text !== action_text) {
        setTimeout(function() {
            $("#footer-status").addClass("appear");
        }, 2);
    }
}
