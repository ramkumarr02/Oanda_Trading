 print('                      PARAMETERS')
    print(f'instrument            : {data["instrument"]}          take_profit_val       : {data["take_profit_val"]}')
    print(f'pip_size              : {data["pip_size"]}           pip_take_profit_ratio : {data["pip_take_profit_ratio"]}') 
    print(f'order_num             : {data["order_num"]}                stop_loss_pip         : {data["stop_loss_pip"]}')
    print(f'timed_loss_windows    : {data["timed_loss_windows"]}                timed_loss_limit      : {round(data["timed_loss_limit"],5)}')
    print(f'act_tick_gap          : {data["act_tick_gap"]}                max_lema_loss         : {round(data["max_lema_loss"],5)}')    

 