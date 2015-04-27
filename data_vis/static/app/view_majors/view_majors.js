'use strict';

angular.module('project1App.viewMajors', ['ngRoute'])

    .config(['$routeProvider', function($routeProvider) {
        $routeProvider.when('/Majors', {
            templateUrl: 'static/app/view_majors/view_majors.html',
            controller: 'ViewMajorsCtrl'
        });
    }])

    .controller('ViewMajorsCtrl', [function($scope) {

    }]);