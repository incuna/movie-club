// jQuery stringify
jQuery.extend({
    stringify  : function stringify(obj) {
        if ("JSON" in window) {
            return JSON.stringify(obj);
        }

        var t = typeof (obj);
        if (t != "object" || obj === null) {
            // simple data type
            if (t == "string") obj = '"' + obj + '"';

            return String(obj);
        } else {
            // recurse array or object
            var n, v, json = [], arr = (obj && obj.constructor == Array);

            for (n in obj) {
                v = obj[n];
                t = typeof(v);
                if (obj.hasOwnProperty(n)) {
                    if (t == "string") {
                        v = '"' + v + '"';
                    } else if (t == "object" && v !== null){
                        v = jQuery.stringify(v);
                    }

                    json.push((arr ? "" : '"' + n + '":') + String(v));
                }
            }

            return (arr ? "[" : "{") + String(json) + (arr ? "]" : "}");
        }
    }
});

$(function() {

    var apiKey = '1db0674dd30f5cb1a979238b9a78b6c4';

    $.ajax({
        url: 'http://api.themoviedb.org/3/configuration',
        data: {
            api_key: apiKey
        },
        dataType: 'json',
        success: function(data) {
            var movieImageUrl = data.images.base_url,
                posterSize = data.images.poster_sizes[0];
            initSearch(movieImageUrl, posterSize);
        }
    });

    var initSearch = function(movieImageUrl, posterSize) {

        var searchResultFormat = function(movie) {
            var movieYear = new Date(movie.release_date).getFullYear(),
                movieFullTitle = movie.title + ' (' + movieYear + ')';
            var markup = '<span class="movie-item"><img src="' + movieImageUrl + posterSize + movie.poster_path + '">' + movieFullTitle + '</span>';

            return markup;
        };
        var searchSelectionFormat = function(movie) {
            $('#movie-data').val(jQuery.stringify(movie));
            var markup = '<span class="movie-item-selected">' + movie.title + '</span>';
            return markup;
        };

        $('#movie-search').select2({
            placeholder: {
                title: 'Search for a movie'
            },
            minimumInputLength: 2,
            ajax: {
                quietMillis: 200,
                url: 'http://api.themoviedb.org/3/search/movie',
                dataType: 'json',
                data: function (term, page) {
                    return {
                        query: term,
                        api_key: apiKey
                    };
                },
                results: function (data, page) {
                    return {
                        results: data.results
                    };
                }
            },
            formatResult: searchResultFormat,
            formatSelection: searchSelectionFormat
        });

    };

});