query:  ((IP* iDominates NP-SBJ*
        AND (IP* iDominates NP-OB1*)
        AND (IP* iDominates NP-OB2*)
        AND (NP-OB1* Precedes NP-OB2*)
        AND (NP-OB1* iDominates !PRO-*)
        AND (NP-OB1* domsWords 2)
        AND (NP-OB2* domsWords 2)))
        -- OR
        -- (IP* iDominates NP-SBJ*
        -- AND (IP* iDominates NP-OB1*)
        -- AND (IP* iDominates NP-OB2*)
        -- AND (NP-OB1* Precedes NP-OB2*)
        -- AND (NP-OB1* iDominates !PRO-*)
        -- AND (NP-OB1* DomsWords 1)
        -- AND (NP-OB2* DomsWords 1))
