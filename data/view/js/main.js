/***************************************
 * View -> Controller
 *  e.g. user input
***************************************/
function send_data(json) {
    var data = JSON.stringify(json);
    document.title = data;
}

/***************************************
 * Controller -> View
 *  e.g. update state
***************************************/
function recv_data(data) {
    switch(data.request) {
        case "queue_update_state":
            send_data({"request": "ping"});
            break;
    }
}

/*****************************
 * Common
*****************************/
var TRANS_SPEED = 300;
var ENABLE_INTRO = true;    // For curated collection

function get_string(string) {
    return LOCALE[string];
}

function get_svg(name) {
    return svg[name];
}

// Returns localised relative or absolute date
function get_date(day, month, year) {
    return day + "/" + month + "/" + year;
}

/*****************************
 * Initialisation
*****************************/
function build_view() {
    // Create the layout of the application

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
                ${_header_button("browse", "boutique-mono")}
                ${_header_button("news", "fa-bullhorn")}
                ${_header_button("search", "fa-search")}
                ${_header_button("queue", "fa-clone")}
                ${_header_button("installed", "fa-download")}
                ${_header_button("settings", "fa-cog")}
            </div>
        </header>
        <content></content>
        <footer>
            <div id="footer-status" onclick="_set_page_queue()" title="${get_string("tooltip_queue")}">
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
    _update_queue_status("ok", get_string("queue_ready"), get_string("queue_ready_state"), 0, -1);

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

    switch(name) {
        case "browse":
            break;
        case "news":
            break;
        case "search":
            break;
        case "queue":
            _set_page_queue();
            break;
        case "installed":
            break;
        case "settings":
            _set_page_settings();
            break;
        default:
            console.error("Invalid page name!");
            break;
    }

    _nav_add_history(name, data);
    CURRENT_PAGE = name;
    CURRENT_PAGE_DATA = data;

    // Enable the back button if this is the first tab.
    if (NAV_HISTORY.length > 1) {
        $("#back-button").removeClass("disabled");
    } else {
        $("#back-button").addClass("disabled");
    }
}

function _nav_add_history(name, data) {
    NAV_HISTORY.push({"name": name, "data": data});
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
