<?php

$output_json = '[' . PHP_EOL;
$temp_path = '/tmp/youtube.html';

exec('wget -O ' . $temp_path . ' https://www.youtube.com/channel/UCU5yJUgbF9E2LxDLS-voY4g/videos');

$youtube_handle = fopen($temp_path, 'r');
if ($youtube_handle) {
    while (($line = fgets($youtube_handle)) !== false) {
        $pattern = '/yt-lockup-title.+/';
        preg_match($pattern, $line, $matches);
        if (sizeof($matches) > 0) {
            $title_pattern = '/title=".+?(?=")"/';
            $href_pattern = '/href=".+?(?=")"/';
            preg_match($title_pattern, $matches[0], $title_match);
            preg_match($href_pattern, $matches[0], $href_match);
            $title_string = str_replace('title=', '"title": ', $title_match[0]);
            $title_string = str_replace('Kaifeck - ', '', $title_string);
            $href_string = str_replace('href=', '"href": ', $href_match[0]);
            $href_string = str_replace('/watch?v=', '', $href_string);
            $output_json .=
                '  {' . PHP_EOL .
                '    ' . $title_string . ',' . PHP_EOL .
                '    ' . $href_string . PHP_EOL .
                '  },' . PHP_EOL;
        }
    }
    echo("Read YouTube Uploads" . PHP_EOL);
} else {
    echo("Error opening " . $temp_path . PHP_EOL);
}

fclose($youtube_handle);
$output_json = rtrim($output_json, PHP_EOL);
$output_json = rtrim($output_json, ',');
$output_json .= PHP_EOL . ']';

$output_path = dirname(__FILE__) . DIRECTORY_SEPARATOR . 'data';
$output_filename = 'youtube_uploads.json';
$output_filepath = $output_path . DIRECTORY_SEPARATOR . $output_filename;

if (!file_exists($output_path)) {
    exec('mkdir ' . $output_path);
}
if (!file_exists($output_filepath)) {
    exec('touch ' . $output_filepath);
}
file_put_contents($output_filepath, $output_json);
