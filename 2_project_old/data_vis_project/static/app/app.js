'use strict';

// Declare app level module which depends on views, and components
angular.module('project1App', [
    'ngRoute',
    'ui.bootstrap',
    'project1App.viewProject1'
]).
    config(['$routeProvider', function($routeProvider) {
        $routeProvider.otherwise({redirectTo: '/Project1'});
    }]);