'use strict';

angular.module('project1App.viewPrograms', ['ngRoute'])

    .config(['$routeProvider', function($routeProvider) {
        $routeProvider.when('/Programs', {
            templateUrl: 'static/app/view_programs/view_programs.html',
            controller: 'ViewProgramsCtrl'
        });
    }])

    .controller('ViewProgramsCtrl', ['$scope', '$http', function($scope, $http) {
        $http.get('/api/program').success(function(data, status) {
            $scope.programs = data;
        });
    }]);