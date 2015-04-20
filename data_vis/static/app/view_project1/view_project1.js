'use strict';

angular.module('project1App.viewProject1', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/Project1', {
    templateUrl: 'static/app/view_project1/view_project1.html',
    controller: 'ViewProject1Ctrl'
  });
}])

.controller('ViewProject1Ctrl', [function($scope) {

}]);