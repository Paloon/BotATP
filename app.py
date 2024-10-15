import discord
from discord.ext import commands
from discord import app_commands
import os
import datetime
from config import Allow_user,Room,Id,Room2,TOKEN
from server import keep_alive


intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix=';',intents=intents)
token = TOKEN

@client.event
async def on_ready():
    global ANOUCE
    ANOUCE = client.get_channel(TAXROOM)
    print(f'เข้าสู่ระบบในฐานะ {client.user}')
    try:
        synced = await client.tree.sync()
        print(f'Synced {len(synced)} command(s).')
    except Exception as e:
        print(f'เกิดข้อผิดพลาดขณะ sync commands: {e}')

Allow_user.append(700563092815347743)
Allow_user.append(1002475625661071411)
ALLOWED_USER_IDS = Allow_user
TAXROOM = int(Room)
ANOUCE = client.get_channel(TAXROOM)

@client.tree.command(name="atp", description="สร้างบัญชีใหม่หรือแจ้งว่ามีอยู่แล้ว")
async def atp_create(interaction: discord.Interaction):
    user = interaction.user
    filename = f"{user.id}.txt"
    
    if os.path.exists(filename):
        content = "คุณมีบัญชีอยู่แล้ว!"
    else:
        content = f"สร้างบัญชีใหม่สำหรับ {user.name}"
        with open(filename, "w") as file:
            file.write("0")
    
    await interaction.response.send_message(content)

# Command to check account balance
@client.tree.command(name="atp_check", description="ตรวจสอบสถานะบัญชีของคุณ")
async def atp_check(interaction: discord.Interaction):
    user = interaction.user
    filename = f"{user.id}.txt"

    if os.path.exists(filename):
        with open(filename, "r") as file:
            content = file.read()
        message = f"ยอดเงินในบัญชีของคุณคือ: {content} หน่วย"
    else:
        message = "คุณยังไม่มีบัญชี กรุณาใช้คำสั่ง /atp เพื่อสร้างบัญชีก่อน"
    
    await interaction.response.send_message(message)

# Command to add money to an account
@client.tree.command(name="atp_add", description="เพิ่มจำนวน API ในบัญชี (เฉพาะแอดมิน)")
@app_commands.describe(amount="จำนวนเงินที่ต้องการเพิ่ม")
async def atp_add(interaction: discord.Interaction, target: discord.Member, amount: int):
    user = target
    filename = f"{user.id}.txt"

    if interaction.user.id not in ALLOWED_USER_IDS:
        await interaction.response.send_message("คุณไม่ได้รับอนุญาตให้ใช้คำสั่งนี้", ephemeral=True)
        return

    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                current_amount = float(file.read())
        except ValueError:
            await interaction.response.send_message("เกิดข้อผิดพลาดในการอ่านจำนวนเงิน กรุณาตรวจสอบไฟล์บัญชี", ephemeral=True)
            return

        new_amount = current_amount + amount
        with open(filename, "w") as file:
            file.write(str(new_amount))
        message = f"เพิ่มจำนวนเงิน {amount} หน่วยให้กับ <@{user.id}> แล้ว ยอดรวม: {new_amount} หน่วย"
    else:
        message = f"<@{user.id}> ยังไม่มีบัญชี กรุณาให้พวกเขาสร้างบัญชีก่อนด้วยคำสั่ง /atp"

    await interaction.response.send_message(message)

# Command to handle tax calculation
@client.tree.command(name="atp_tax", description="ตรวจสอบและจ่ายภาษี")
async def atp_tax(interaction: discord.Interaction):
    user = interaction.user
    filename = f"{user.id}.txt"
    current_month = datetime.datetime.now().strftime("%B")

    if os.path.exists(filename):
        with open(filename, "r") as file:
            atp = float(file.read())
            tax = atp * 0.05
            result = atp - tax
        with open(filename, "w") as file:
            file.write(str(result))
        message = (
            f"จ่ายภาษีสำหรับเดือน {current_month} ไปแล้ว: {tax} API"
            f"ยอดเงินในบัญชีของคุณคือ: {result} API"
        )
    else:
        message = "คุณยังไม่มีบัญชี กรุณาใช้คำสั่ง /atp เพื่อสร้างบัญชีก่อน"
    
    await interaction.response.send_message(message)
    if ANOUCE:
        await ANOUCE.send(f"{user.mention} ได้ทำการจ่ายภาษีของเดือน {current_month} เรียบร้อย")

# Command to transfer money between users
@client.tree.command(name="atp_transfer", description="โอนจำนวนเงินของคุณให้กับคนอื่น")
@app_commands.describe(amount="จำนวนเงินที่ต้องการโอน")
async def atp_transfer(interaction: discord.Interaction, target: discord.Member, amount: int):
    sender = interaction.user
    receiver = target
    sender_file = f"{sender.id}.txt"
    receiver_file = f"{receiver.id}.txt"

    if sender == receiver:
        await interaction.response.send_message("คุณไม่สามารถโอนเงินให้ตัวเองได้", ephemeral=True)
        return

    if not os.path.exists(sender_file):
        await interaction.response.send_message("คุณยังไม่มีบัญชี กรุณาใช้คำสั่ง /atp เพื่อสร้างบัญชีก่อน", ephemeral=True)
        return

    if not os.path.exists(receiver_file):
        await interaction.response.send_message(f"{receiver.name} ยังไม่มีบัญชี", ephemeral=True)
        return

    try:
        with open(sender_file, "r") as file:
            sender_balance = float(file.read())

        with open(receiver_file, "r") as file:
            receiver_balance = float(file.read())
    except ValueError:
        await interaction.response.send_message("เกิดข้อผิดพลาดในการอ่านจำนวน API", ephemeral=True)
        return

    if sender_balance < amount:
        await interaction.response.send_message("ยอดเงินของคุณไม่เพียงพอ", ephemeral=True)
        return

    sender_balance -= amount
    receiver_balance += amount

    with open(sender_file, "w") as file:
        file.write(str(sender_balance))

    with open(receiver_file, "w") as file:
        file.write(str(receiver_balance))

    message = f"โอนAPI {amount} API ให้กับ {receiver.mention} แล้ว ยอดเงินคงเหลือ: {sender_balance} API"
    await interaction.response.send_message(message)

@client.tree.command(name="atp_revoke", description="ถอนจำนวน API ออกจากบัญชีของคุณ [ไม่มีการคืน ATP หากถอนหลายครั่งต่อวัน]")
@app_commands.describe(account_number="เลขบัญชี 10 ตัว", amount="จำนวนที่ต้องการถอน (สูงสุด 100 ATP)")
async def atp_revoke(interaction: discord.Interaction, account_number: str, amount: int):
    user = interaction.user
    admin_user_id = Id
    filename = f"{user.id}.txt"

    if len(account_number) != 10 or not account_number.isdigit():
        await interaction.response.send_message("กรุณาใส่เลขบัญชีที่ถูกต้อง (10 ตัวเลข)", ephemeral=True)
        return

    if amount > 100:
        await interaction.response.send_message("จำนวนที่ถอนต้องไม่เกิน 100 API", ephemeral=True)
        return

    if not os.path.exists(filename):
        await interaction.response.send_message("คุณยังไม่มีบัญชี กรุณาใช้คำสั่ง /atp เพื่อสร้างบัญชีก่อน", ephemeral=True)
        return

    try:
        with open(filename, "r") as file:
            current_balance = float(file.read())
    except ValueError:
        await interaction.response.send_message("เกิดข้อผิดพลาดในการอ่านยอด API ของคุณ", ephemeral=True)
        return

    if current_balance < amount:
        await interaction.response.send_message("ยอด API ในบัญชีของคุณไม่เพียงพอ", ephemeral=True)
        return

    new_balance = current_balance - amount
    with open(filename, "w") as file:
        file.write(str(new_balance))

    amount_in_thb = amount / 10

    admin_user = await client.fetch_user(admin_user_id)
    if admin_user:
        withdrawal_message = (
            f"ผู้ใช้ {user.name} ได้ทำการถอนเงิน {amount} หน่วย (ATP)\n"
            f"ยอดเงินเท่ากับ {amount_in_thb} บาท (1 ATP = 10 บาท)\n"
            f"เลขบัญชีที่ใช้ในการถอน: {account_number}"
        )
        await admin_user.send(withdrawal_message)

    await interaction.response.send_message(
        f"กำลังดำเนินการ ยอดคงเหลือ: {new_balance} ATP"
    )

@client.tree.command(name="atp_revoke_success", description="แจ้งเตือนการถอนเงินสำเร็จ")
@app_commands.describe(member="สมาชิกที่ทำการถอนเงิน", value="จำนวนเงินที่ถอนสำเร็จ")
async def atp_revoke_success(interaction: discord.Interaction, member: discord.Member, value: int):
    admin_user_id = Id
    notify_channel_id = Room2

    if interaction.user.id != admin_user_id:
        await interaction.response.send_message("คุณไม่ได้รับอนุญาตให้ใช้คำสั่งนี้", ephemeral=True)
        return

    if value <= 0:
        await interaction.response.send_message("กรุณาใส่จำนวนเงินที่ถูกต้อง", ephemeral=True)
        return

    notify_channel = client.get_channel(notify_channel_id)
    if not notify_channel:
        await interaction.response.send_message("ไม่พบช่องสำหรับส่งการแจ้งเตือน", ephemeral=True)
        return

    success_message = f"{member.mention} ได้ทำการถอนเงินสำเร็จเป็นจำนวนเงิน {value} บาท"
    await notify_channel.send(success_message)

    await interaction.response.send_message(f"การแจ้งเตือนถอนเงินสำหรับ {member.mention} ได้ถูกส่งเรียบร้อยแล้ว", ephemeral=True)

@client.tree.command(name="atp_balances", description="ดูยอดเงินของผู้ใช้ทุกคน (เฉพาะแอดมิน)")
async def atp_balances(interaction: discord.Interaction):
    if interaction.user.id not in ALLOWED_USER_IDS:
        await interaction.response.send_message("คุณไม่ได้รับอนุญาตให้ใช้คำสั่งนี้", ephemeral=True)
        return

    balances = []
    for member in interaction.guild.members:
        filename = f"{member.id}.txt"
        if os.path.exists(filename):
            with open(filename, "r") as file:
                balance = file.read()
            balances.append(f"{member.display_name}: {balance} หน่วย")
    await interaction.response.send_message("\n".join(balances), ephemeral=True)

@client.tree.command(name="atp_force_transfer", description="บังคับโอนเงินระหว่างสองบัญชี (เฉพาะแอดมิน)")
async def atp_force_transfer(interaction: discord.Interaction, from_user: discord.Member, to_user: discord.Member, amount: int):
    if interaction.user.id not in ALLOWED_USER_IDS:
        await interaction.response.send_message("คุณไม่ได้รับอนุญาตให้ใช้คำสั่งนี้", ephemeral=True)
        return

    from_file = f"{from_user.id}.txt"
    to_file = f"{to_user.id}.txt"

    if os.path.exists(from_file) and os.path.exists(to_file):
        with open(from_file, "r") as file:
            from_balance = float(file.read())
        if from_balance >= amount:
            new_from_balance = from_balance - amount
            with open(from_file, "w") as file:
                file.write(str(new_from_balance))

            with open(to_file, "r") as file:
                to_balance = float(file.read())
            new_to_balance = to_balance + amount
            with open(to_file, "w") as file:
                file.write(str(new_to_balance))

            await interaction.response.send_message(f"โอนเงิน {amount} หน่วยจาก {from_user.display_name} ไปยัง {to_user.display_name} เรียบร้อยแล้ว")
        else:
            await interaction.response.send_message(f"{from_user.display_name} มียอดเงินไม่เพียงพอ", ephemeral=True)
    else:
        await interaction.response.send_message("หนึ่งในผู้ใช้นี้ยังไม่มีบัญชี", ephemeral=True)

keep_alive()
client.run(token)