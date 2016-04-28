var app = angular.module('cs467',['ngRoute', 'cs467Controllers']).
config(function ($routeProvider) {
	$routeProvider.otherwise({
		redirectTo: '/list'
	});
})
