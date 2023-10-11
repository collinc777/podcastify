"use client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { WineOff } from "lucide-react";
import { useState } from "react";

export const URLForm = () => {
  const [url, setUrl] = useState<string>("");
  const onSubmit = async () => {
    // fetch html from url
    console.log({ url });
    const response = await fetch(`/api/generate_script?url=${url}`, {
      method: "POST",
    });
    const blob = await response.blob();
    const objectURl = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = objectURl;
    link.setAttribute("download", "audio.mp3");
    document.body.appendChild(link);
    link.click();
  };
  return (
    <>
      <Label htmlFor="url">Url</Label>
      <Input
        type="url"
        value={url}
        onChange={(val) => setUrl(val.target.value)}
      />
      <Button type="submit" onClick={onSubmit}>
        Submit
      </Button>
    </>
  );
};
