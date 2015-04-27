'use strict';

angular.module('project1App.viewHome', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/', {
    templateUrl: 'static/app/view_home/view_home.html',
    controller: 'ViewHomeCtrl'
  });
}])

.controller('ViewHomeCtrl', [function($scope) {

}]);