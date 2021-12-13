<?php
    class user {
        public string $username;
        public bool $admin;
        public string $profile_img;

        function __construct(){
            $this->username = "guest";
            $this->admin = false;
            $this->profile_img = "/var/www/html/guest.png";
        }

        function __destruct(){
            clearstatcache();
            if ($this->admin === true){
                echo("<html><p>Did you think it was going to be that easy? Right idea, wrong approach :)</p></html>\r\n");
            }
            else{
                if (file_exists($this->profile_img) === false){
                    echo("<html><p><b>Getting impatient? For only $20000000 you can have the answer right now. Just call up our hotline at (888)-TRY-HARDR!</b></p><p>Hint: The file exists under the <b>/</b> directory as <b>flag.png</b>. Can you find a way to reach it?</p></html>\r\n");
                }
                else {
                    if(substr($this->profile_img, 0, 14) === "/var/www/html/"){
                        $size = filesize($this->profile_img);
                        $file_contents = file_get_contents($this->profile_img, false, null, 0);

                        header('Content-Type: image/png');
                        header("Content-length: $size");
                        echo($file_contents);
                    }
                    else{
                        echo("<html><p><b>Getting impatient? For only $5000000 you can have the answer right now. Just call up our hotline at (888)-TRY-HARDZ!</b></p><p>Attempt to read outside of /var/www/html detected! Try Harder!</p><p>Hint: The file exists under the <b>/</b> directory as <b>flag.png</b>. Can you find a way to reach it?</p></html>\r\n");
                    }
                }
            }
            clearstatcache();
        }
    };

    if (array_key_exists('user', $_COOKIE)) {
        $raw_cookie = base64_decode(base64_decode($_COOKIE['user']));
        try {
            $userObj = unserialize($raw_cookie, ["allowed_classes" => ["user"]]); // https://www.tutorialspoint.com/php7/php7_filtered_unserialize.htm said this was safe
        }
        catch (Exception $e){
            echo("<p>Hint: The file exists under the <b>/</b> directory as <b>flag.png</b>. Can you find a way to reach it?</p></html>\r\n");
        }
        if ($userObj == false){
            echo("<p>Hint: The file exists under the <b>/</b> directory as <b>flag.png</b>. Can you find a way to reach it?</p></html>\r\n");
        }
    }
    else {
        $userObj = new user();
        $userObjSerial = serialize($userObj);
        setcookie('user', base64_encode(base64_encode($userObjSerial)), 0, "/");
    }

