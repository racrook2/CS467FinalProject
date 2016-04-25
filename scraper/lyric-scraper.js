var fs = require('fs');
var request = require('request');
var cheerio = require('cheerio');

/*

Module that takes an artist and a list of songs, and scrapes the lyrics for them. Will write lyrics into respective artist directory
and file. Directory and file are created if they do not exist.

*/

var scrapeLyrics = function(artist, songs){
  for (song in songs) {
    var data = "";
    var first = artist.charAt(0);
    var newSong = songs[song].replace(/ /g, "-");
    var url = 'http://www.metrolyrics.com/'+newSong+'-lyrics-'+artist+'.html';

    if(!fs.existsSync('data/'+artist+'/')){
      fs.mkdirSync('data/'+artist+'/');
    }
    try{
      var fileStatus = fs.accessSync('data/'+artist+'/'+newSong+'.txt');
      console.log("File exists");
    } catch(e){
      fs.openSync('data/'+artist+'/'+newSong+'.txt', 'w');
      request(url, ( function(newSong) {
        return function(error, response, html){
          if(!error){
            var $ = cheerio.load(html);
            var json = $('#lyrics #lyrics-main div div #lyrics-body div div#lyrics-body-text');

            $(json.children()).each(function(i, elm) {
                fs.appendFileSync('data/'+artist+'/'+newSong+'.txt', $(this).text());
            });
          }
        }  
      })(newSong));
    }
  }
}

module.exports.scrapeLyrics = scrapeLyrics;