'use strict';

// Declare app level module which depends on views, and components
angular.module('project1App', [
    'ngRoute',
    'ui.bootstrap',
    'project1App.viewHome',
    'project1App.viewPrograms',
    'project1App.viewMajors'
]).
    config(['$routeProvider', function($routeProvider) {
        $routeProvider.otherwise({redirectTo: '/'});
    }]);