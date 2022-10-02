/*
 * View model for OctoPrint-OctoRant
 *
 * Author: Benjamin Chanudet
 * License: MIT
 */
$(function() {
    function OctorantViewModel(parameters) {
        var self = this;
    }

    // view model class, parameters for constructor, container to bind to
    OCTOPRINT_VIEWMODELS.push({
        construct: OctorantViewModel,
        //dependencies: [ "loginStateViewModel", "settingsViewModel" ],
    });
});
