var mp3Controllers = angular.module('cs467Controllers', []).
controller('MainCtrl', ['$scope', '$http', '$location', '$anchorScroll',
	function($scope, $http, $location, $anchorScroll) {
		$scope.alphabet = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B',
						   'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
						   'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
		
		$http.get('./data/songs').success(function(data) {
			$scope.songs = data;
			$scope.songs_sorted = [];
			for (var i = 0; i < $scope.songs.length; i++) {
				$scope.songs_sorted.push([$scope.songs[i]['name'], $scope.songs[i]['sentiment']]);
			}
			$scope.songs_sorted.sort(function(a, b) {
				return a[1] - b[1];
			});
			$scope.songs_sorted = $scope.songs_sorted.reverse();
		});
		
		$http.get('./data/keywords').success(function(data) {
			$scope.keywords = data;
			var keywords_sorted1 = [];
			var keywords_sorted2 = [];
			for (keyword in $scope.keywords) {
				keywords_sorted1.push([keyword, $scope.keywords[keyword][0]]);
				keywords_sorted2.push([keyword, $scope.keywords[keyword][1]]);
			}
			keywords_sorted1.sort(function(a, b) {
				return a[1] - b[1];
			});
			keywords_sorted2.sort(function(a, b) {
				return a[1] - b[1];
			});
			$scope.keywords = keywords_sorted1.reverse();
			$scope.keywords2 = keywords_sorted2.reverse();
		});
		
		$scope.getColor = function(index) {
			var green = Math.round(Math.min((255.0 * 2.0) * (index/($scope.keywords.length - 1)), 255));
			var red = Math.round(Math.min((255.0 * 2.0) * (($scope.keywords.length - 1 - index)/($scope.keywords.length - 1))));
			return "" + green + ", " + red + ", 0";
		};
		
		$scope.getColor2 = function(index) {
			var green = Math.round(Math.min((255.0 * 2.0) * (index/($scope.songs.length - 1)), 255));
			var red = Math.round(Math.min((255.0 * 2.0) * (($scope.songs.length - 1 - index)/($scope.songs.length - 1))));
			return "" + green + ", " + red + ", 0";
		};
		
		$scope.findValue = function(keyword) {
			for (var i = 0; i < $scope.keywords.length; i++) {
				if ($scope.keywords[i][0] == keyword) return i;
			}
			return -1;
		};
		
		$scope.findValue2 = function(song) {
			for (var i = 0; i < $scope.songs_sorted.length; i++) {
				if ($scope.songs_sorted[i][0] == song) return i;
			}
			return -1;
		};
		
		$scope.scrollTo = function(id) {
			$location.hash(id);
			console.log($location.hash());
			$anchorScroll();
		};
	}
]);
