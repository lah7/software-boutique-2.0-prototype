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
var CURRENT_TAB = "undefined";

function get_string(string) {
    return LOCALE[string];
}

function get_svg(name) {
    return svg[name];
}

/*****************************
 * Initialisation
*****************************/
function build_view() {
    // Create the layout of the application

    // -- 1. Header
    function _header_button(fn, image, string) {
        return `<button id="tab-button-${string}" class="nav-button" onclick="${fn}" title="${get_string("tooltip_" + string)}">
            ${get_svg(image)}
            <span>${get_string(string)}</span>
        </button>`;
    }

    $("body").prepend(`
        <header>
            <div class="left">
                <button id="back-button" class="disabled" onclick="go_back()" title="${get_string("tooltip_back")}">${get_svg("fa-chevron-left")}</button>
                <div class="title"></div>
            </div>

            <div class="right">
                ${_header_button("tab_browse()", "boutique-mono", "browse")}
                ${_header_button("tab_news()", "fa-newspaper", "news")}
                ${_header_button("tab_search()", "fa-search", "search")}
                ${_header_button("tab_queue()", "fa-clone", "queue")}
                ${_header_button("tab_installed()", "fa-download", "installed")}
                ${_header_button("tab_settings()", "fa-cog", "settings")}
            </div>
        </header>
        <content></content>
        <footer>
            <div class="status" onclick="tab_queue()">
                <div id="status-icon" class="positive"></div>
                <div id="status-text">
                    <div class="progress-text">${get_string('app_ready')}</div>
                    <div class="progress-subtext"></div>
                    <progress id="progress-bar"></progress>
                </div>
            </div>
        </footer>
    `);

    $("body").show();
    _update_queue_button();

    // Open default tab
    // ????
}
