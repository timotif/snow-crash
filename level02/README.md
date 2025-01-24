## level02

We are presented with a `pcap` file.

<aside>
💡

Packet capture is a networking practice involving the interception of data packets travelling over a network. Once the packets are captured, they can be stored by IT teams for further analysis. The inspection of these packets allows IT teams to identify issues and solve network problems affecting daily operations.

</aside>

The most common tool used to work on these packets is Wireshark.

With Right Click→Follow→TCP Stream we get to see the whole “conversation”. There’s a bit that seems promising:

```bash
Password: 
ft_wandr...NDRel.L0L
```

Some characters are not printable, so let’s see what they really are with the HexDump view:

```bash
000000B9  66                                                 f
000000BA  74                                                 t
000000BB  5f                                                 _
000000BC  77                                                 w
000000BD  61                                                 a
000000BE  6e                                                 n
000000BF  64                                                 d
000000C0  72                                                 r
000000C1  7f                                                 .
000000C2  7f                                                 .
000000C3  7f                                                 .
000000C4  4e                                                 N
000000C5  44                                                 D
000000C6  52                                                 R
000000C7  65                                                 e
000000C8  6c                                                 l
000000C9  7f                                                 .
000000CA  4c                                                 L
000000CB  30                                                 0
000000CC  4c                                                 L
000000CD  0d                                                 .
```

`7f` is `del`. Let’s try to reconstruct what was actually typed: 

ft_wandr`<del x3>`NDRel`<del>`L0L`<enter>` which adds up to `ft_waNDReL0L` .

That’s the password for `flag02`!

```bash
level02@SnowCrash:~$ su flag02
Password: 
Don't forget to launch getflag !
flag02@SnowCrash:~$ getflag
Check flag.Here is your token : kooda2puivaav1idi4f57q8iq
```

### External resources
- Wireshark (https://www.wireshark.org/)

### Key Learnings
- TCP dump exploration
- Password sniffing