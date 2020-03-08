//
// Settings - if the user wishes to make changes to the UI and behaviour
//            of the Software Boutique.
//
// Actual data set at app start.
var SETTINGS = {};


/*************************************************
 * Send update to the controller.
*************************************************/
// Set an individual key with a new value.
function settings_set_key(key, value) {
    SETTINGS[key] = value;
    send_data("settings_set_key", {
        "key": key,
        "value": value
    });
}

/*************************************************
 * Received update from the controller.
*************************************************/
// Controller does not respond.

/*************************************************
 * Internal view functions to update the page.
*************************************************/
function set_page_settings() {
    var has_index = SETTINGS.index.available;
    var has_index_style = has_index ? "" : "style='display:none'";

    $("content").html(`
        <div class="settings-page">
            <row>
                <left>
                    ${get_string("about")}
                </left>
                <right>
                    <group class="about">
                        ${get_svg("boutique-mono")}
                        <div>
                            ${get_string("ver_software")}
                            <help>
                                ${SETTINGS.version.boutique}
                            </help>
                        </div>
                    </group>
                    <p ${has_index_style}>
                        ${get_string("index_about")}
                    </p>
                    <group class="about" ${has_index_style}>
                        <img src="../index/distro-logo.svg"/>
                        <div>
                            ${SETTINGS.index.name}
                            <help>
                                ${get_string("ver_index").replace("123", SETTINGS.index.revision)}
                                <br>
                                ${get_string("last_updated").replace("[]", get_date(SETTINGS.index.timestamp))}
                            </help>
                        </div>
                    </group>
                    <p ${has_index_style}>
                        <button onclick="open_uri('${SETTINGS.index.info_url}')" title="${SETTINGS.index.info_url}">${get_string("index_info_url")}</button>
                        <button onclick="open_uri('${SETTINGS.index.support_url}')" title="${SETTINGS.index.support_url}">${get_string("index_support_url")}</button>
                    </p>
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
                                <td>${SETTINGS.backends.snap ? get_string("backend_working") : get_string("backend_not_working")}</td>
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
                    <group ${has_index_style}>
                        <label>
                            <input type="checkbox" onclick="settings_set_key('hide_proprietary', this.checked)" ${SETTINGS.hide_proprietary === true ? "checked" : ""}/>
                            ${get_string("hide_proprietary")}
                        </label>
                    </group>

                    <group>
                        <label>
                            <input type="checkbox" onclick="settings_set_key('show_advanced', this.checked)" ${SETTINGS.show_advanced === true ? "checked" : ""}/>
                            ${get_string("show_advanced")}
                        </label>
                    </group>

                    <group>
                        <label>
                            <input type="checkbox" onclick="settings_set_key('precise_time', this.checked)" ${SETTINGS.precise_time === true ? "checked" : ""}/>
                            ${get_string("precise_time")}
                        </label>
                    </group>

                    <group>
                        <label>
                            <input type="checkbox" onclick="settings_set_key('compact_list', this.checked)" ${SETTINGS.compact_list === true ? "checked" : ""}/>
                            ${get_string("compact_list")}
                        </label>
                    </group>

                </right>
            </row>
            <row ${has_index_style}>
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
