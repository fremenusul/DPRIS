def rankBuilder(rank):
    if rank == 'PV2':
        return 'PFC'
    elif rank == 'PFC':
        return 'SPC'
    elif rank == 'SPC':
        return 'CPL'
    elif rank == 'CPL':
        return 'SGT'
    elif rank == 'SGT':
        return 'SSG'
    elif rank == 'SSG':
        return 'SFC'
    elif rank == 'SFC':
        return 'MSG'
    elif rank == 'MSG':
        return '1SG'
    elif rank == '1SG':
        return 'SGM'
    elif rank == 'SGM':
        return '2LT'
    elif rank == '2LT':
        return '1LT'
    elif rank == '1LT':
        return 'CPT'
    elif rank == 'CPT':
        return 'MAJ'
    elif rank == 'MAJ':
        return 'LTC'
