# -*- coding: utf-8 -*-

import config
import renren

if __name__ == "__main__":

    my_account = renren.Renren()
    my_account.login(config.EMAIL, config.PASSWORD, '')
