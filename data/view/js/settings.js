// Settings Array - should be updated when application runs.
var SETTINGS = {
    // Read-only
    "version": {
        "boutique": "?.?.?-dev",
        "index": 0
    },
    "index": {
        "day": 31,
        "month": 12,
        "year": 2019
    },
    "backends": {
        "apt": false,
        "snap": false,
        "appstream": false
    },

    // Settings - simple key/value structure
    "hide_proprietary": false,
    "show_advanced": false,
    "precise_time": false
};

/*************************************************
 * Send update to the controller.
*************************************************/
// Retrieve current settings list.
function settings_get_data() {
    send_data({
        "request": "settings_get_data"
    });
}

// Set an individual key with a new value.
function settings_set_key(key, value) {
    send_data({
        "request": "settings_set_key",
        "key": key,
        "value": value
    });
}

/*************************************************
 * Received update from the controller.
*************************************************/
function settings_recv_data(data) {
    // Callback when the controller has gathered the settings list.
    //
    // Variable         Example                 Description
    // ---------------- ----------------------- -----------------------------------
    // request          settings_recv_data      Required
    // data             {"prop1": true}         Dictonary containing key data.

    SETTINGS = JSON.parse(data.data);
}

/*************************************************
 * Internal view functions to update the page.
*************************************************/
function _set_page_settings() {
    $("content").html(`
        <div class="settings-page">
            <row>
                <left>
                    ${get_string("about")}
                </left>
                <right>
                    <group>
                        ${get_string("ver_software").replace("2.0", SETTINGS.version.boutique)}
                    </group>
                    <group>
                        ${get_string("ver_index").replace("123", SETTINGS.version.index)}
                        <help>
                            ${get_string("last_updated").replace("[]", get_date(SETTINGS.index.day, SETTINGS.index.month, SETTINGS.index.year))}
                        </help>
                    </group>
                </right>
            </row>
            <row>
                <left>
                    ${get_string("backend")}
                </left>
                <right>
                    <table>
                        <tbody>
                            <tr>
                                <th>${get_string("backend_apt")}</th>
                                <td>${SETTINGS.backends.apt ? get_string("backend_working") : get_string("backend_not_working")}</td>
                            </tr>
                            <tr>
                                <th>${get_string("backend_snap")}</th>
                                <td>${SETTINGS.backend_snap ? get_string("backend_working") : get_string("backend_not_working")}</td>
                            </tr>
                            <tr>
                                <th>${get_string("backend_appstream")}</th>
                                <td>${SETTINGS.backends.appstream ? get_string("backend_working") : get_string("backend_not_working")}</td>
                            </tr>
                        </tbody>
                    </table>
                </right>
            </row>
            <row>
                <left>
                    ${get_string("interface")}
                </left>
                <right>
                    <group>
                        <label>
                            <input type="checkbox" onclick="settings_set_key('hide_proprietary', this.checked)"/>
                            ${get_string("hide_proprietary")}
                        </label>
                        <help>${get_string("hide_proprietary_help")}</help>
                    </group>

                    <group>
                        <label>
                            <input type="checkbox" onclick="settings_set_key('show_advanced', this.checked)"/>
                            ${get_string("show_advanced")}
                        </label>
                        <help>${get_string("show_advanced_help")}</help>
                    </group>

                    <group>
                        <label>
                            <input type="checkbox" onclick="settings_set_key('precise_time', this.checked)"/>
                            ${get_string("precise_time")}
                        </label>
                        <help>${get_string("precise_time_help")}</help>
                    </group>
                </right>
            </row>
            <row ${ENABLE_INTRO == false ? "hidden" : ""}>
                <left>
                    ${get_string("misc")}
                </left>
                <right>
                    <button onclick="show_intro()">${get_string("show_intro")}</button>
                </right>
            </row>
        </div>
    `);
}
