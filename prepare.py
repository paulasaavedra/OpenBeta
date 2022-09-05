# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 10:32:44 2021

@author: paula
"""

from brainflow.board_shim import BoardShim, BrainFlowInputParams

def prepare(board_id,port=None):
    """
    initialize processes needed to start reading the board.

    Parameters
    ----------
    board_id : int
        Integer that determines which board is used:
            Synthetic: -1
            Cyton: 0
            Ganglion: 1
            Cyton Daisy: 2
            
    port : string, opcional
        Port where the dongle is connected. Default: None
            Synthetic: None
            Cyton, Ganglion, Cyton Daisy, verify.
            
    Returns
    -------
    board : board_shim.BoardShim
        brainflow.board_shim object
        allows to read the board.

    """

    BoardShim.enable_dev_board_logger ()
    params = BrainFlowInputParams ()
    params.serial_port = port
    board = BoardShim (board_id,params)
    return (board)  


    

