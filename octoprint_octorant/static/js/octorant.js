/*
 * View model for OctoPrint-OctoRant
 *
 * Author: Benjamin Chanudet
 * License: MIT
 */
$(function() {
    function OctorantViewModel(parameters) {
        var self = this;
        self.settings = parameters[1];

        self.categories = ["system","printer","prints","transfers","progress","timelapses"];
        self.events = null;

        self.onBeforeBinding = () => {
            self.events = self.settings.settings.plugins.octorant.events;
        }
    }

    // view model class, parameters for constructor, container to bind to
    OCTOPRINT_VIEWMODELS.push({
        construct: OctorantViewModel,
        dependencies: [ "loginStateViewModel", "settingsViewModel" ],
        elements: ["div#settings_plugin_octorant"]
    });
});
