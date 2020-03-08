/**********************************************
 * View -> Controller | such as for user input
**********************************************/
function send_data(request, json) {
    //
    // Sends JSON data to the Controller.
    //
    //  request     String of the Python function to run.
    //  json        JSON data.
    //
    json["request"] = request;
    var data = JSON.stringify(json);
    document.title = data;
}

/***********************************************
 * Controller -> View | such as updating status
***********************************************/
function recv_data(data) {
    switch(data.request) {
        // queue.js
        case "update_queue_list":
            update_queue_list(data);
            break;
        case "update_queue_state":
            update_queue_state(data);
            break;

        // app.js
        case "populate_app_list":
            populate_app_list(data);
            break;
        case "open_app_details":
            open_app_details(data);
            break;
    }
}

/*****************************
 * Common
*****************************/
// Set at app start
var LOCALE;
var SVGS;

// Global variables
var TRANS_SPEED = 300;

function get_string(string) {
    return LOCALE[string];
}

function get_svg(name) {
    return SVGS[name];
}

function open_uri(uri) {
    send_data("open_uri", {
        "uri": uri
    });
}

function get_date(seconds) {
    var t = new Date(1970, 0, 1); // Epoch
    t.setSeconds(seconds);

    // TODO: Implement rellative/absolute logic
    return t.toDateString()
}

function get_random_element_id() {
    var time = new Date().getTime();
    return "id-" + time;
}

/*****************************
 * Initialisation
*****************************/
function build_view() {
    //
    // Create the layout of the application
    //
    var has_index = SETTINGS.index.available;

    // -- 1. Header
    function _header_button(string, image) {
        return `<button id="nav-button-${string}" class="nav-button" onclick="change_page('${string}')" title="${get_string("tooltip_" + string)}">
            ${get_svg(image)}
            <span>${get_string(string)}</span>
        </button>`;
    }

    $("body").prepend(`
        <header>
            <div class="left">
                <button id="back-button" class="disabled" onclick="nav_go_back()" title="${get_string("tooltip_back")}">${get_svg("fa-chevron-left")}</button>
                <div id="header-title" class="title"></div>
            </div>

            <div class="right">
                ${has_index ? _header_button("browse", "boutique-mono") : ""}
                ${has_index ? _header_button("news", "fa-bullhorn") : ""}
                ${_header_button("search", "fa-search")}
                ${_header_button("queue", "fa-clone")}
                ${_header_button("installed", "fa-download")}
                ${_header_button("settings", "fa-cog")}
            </div>
        </header>
        <content></content>
        <footer>
            <div id="footer-status" onclick="change_page('queue')" title="${get_string("tooltip_queue")}">
                <div id="status-icon"></div>
                <div id="status-text">
                    <div id="progress-text"></div>
                    <div id="progress-subtext"></div>
                    <progress id="progress-bar"></progress>
                </div>
            </div>
        </footer>
    `);

    $("body").show();
    _update_queue_button();
    _update_queue_state("ok", get_string("queue_ready"), get_string("queue_ready_state"), 0, -1);

    // Open default tab
    // TODO: Add user option to change this later.
    change_page("browse");
}

/*****************************
 * Navigation
*****************************/
var NAV_HISTORY = [];
var CURRENT_PAGE = "";
var CURRENT_PAGE_DATA = undefined;

// 'Tab memory' is to remember the state, e.g. search results,
// an app that was open or a request to the controller that would be
// triggered again.

function change_title(new_title) {
    $("#header-title").html(new_title);
}

function change_page(name, data) {
    $(".nav-button").removeClass("active");
    $("#nav-button-" + name).addClass("active");
    change_title(get_string("title_" + name));

    _nav_add_history(name, data);
    CURRENT_PAGE = name;
    CURRENT_PAGE_DATA = data;

    switch(name) {
        case "browse":
            set_tab_browse(data);
            break;
        case "news":
            break;
        case "search":
            break;
        case "queue":
            set_page_queue();
            break;
        case "installed":
            break;
        case "settings":
            set_page_settings();
            break;
        case "details":
            set_page_details(data);
            break;
        default:
            console.error("Invalid page name!");
            break;
    }
}

function _nav_add_history(name, data) {
    NAV_HISTORY.push({"name": name, "data": data});
    _nav_refresh_back_btn();
}

function _nav_refresh_back_btn() {
    // Enable the back button if this is the first tab.
    if (NAV_HISTORY.length > 1) {
        $("#back-button").removeClass("disabled");
    } else {
        $("#back-button").addClass("disabled");
    }
}

function nav_go_back() {
    // Discard current tab/data.
    NAV_HISTORY.pop();

    // Load new tab (pop again as it will be re-added again)
    CURRENT_PAGE = NAV_HISTORY[NAV_HISTORY.length - 1].name;
    CURRENT_PAGE_DATA = NAV_HISTORY[NAV_HISTORY.length - 1].data;
    NAV_HISTORY.pop();
    change_page(CURRENT_PAGE, CURRENT_PAGE_DATA);
}
