"use client";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Loader2, WineOff } from "lucide-react";
import { useState } from "react";
import * as z from "zod";

const formSchema = z.object({
  url: z.string().min(1),
});
import { zodResolver } from "@hookform/resolvers/zod";
import { SubmitHandler, useForm } from "react-hook-form";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";

export const URLForm = () => {
  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      url: "",
    },
  });
  const onSubmit: SubmitHandler<z.infer<typeof formSchema>> = async (
    values,
    _event
  ) => {
    // fetch html from url
    const url = values.url;
    const response = await fetch(`/api/generate_script?url=${url}`, {
      method: "POST",
    });
    if (response.status !== 200) {
    } else {
      const blob = await response.blob();
      const objectURl = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = objectURl;
      link.setAttribute("download", "audio.mp3");
      document.body.appendChild(link);
      link.click();
      return;
    }
  };
  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <Card>
          <CardHeader>
            <CardTitle>Turn Articles into Podcasts</CardTitle>
          </CardHeader>
          <CardContent>
            <FormField
              name="url"
              control={form.control}
              render={({ field }) => {
                return (
                  <FormItem>
                    <FormLabel>Article Url</FormLabel>
                    <FormControl>
                      <Input
                        {...field}
                        placeholder="https://www.nasa.gov/history/july-20-1969-one-giant-leap-for-mankind/"
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                );
              }}
            />
          </CardContent>
          <CardFooter>
            {form.formState.isLoading || form.formState.isSubmitting ? (
              <Button type="submit" disabled>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Generating Episode. Takes a minute or two.
              </Button>
            ) : (
              <Button type="submit">Submit</Button>
            )}
          </CardFooter>
        </Card>
      </form>
    </Form>
  );
};
