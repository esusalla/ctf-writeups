<?php
class CommandModel
{
    public function __construct($url)
    {
        $this->command = "curl -sL " . escapeshellcmd($url);
        print $this->command;
    }

    public function exec()
    {
        exec($this->command, $output);
        return $output;
    }
}
